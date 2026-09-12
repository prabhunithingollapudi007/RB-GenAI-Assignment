"""Semantic similarity analysis for paired human and AI answers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "paired_answers_clean.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_MODEL = "sentence-transformers/all-mpnet-base-v2"
REQUIRED_COLUMNS = {
    "Person ID", "Question Category", "Question Text", "Human Answer", "AI Answer"
}


def load_pairs(input_file: Path = INPUT_FILE) -> pd.DataFrame:
    pairs = pd.read_csv(input_file)
    missing_columns = REQUIRED_COLUMNS.difference(pairs.columns)
    if missing_columns:
        raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")
    return pairs


def embed_pairs(pairs: pd.DataFrame, model_name: str = DEFAULT_MODEL) -> pd.DataFrame:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as error:
        raise RuntimeError(
            "Install the semantic extra first: pip install -e '.[semantic]'"
        ) from error

    model = SentenceTransformer(model_name)
    human_embeddings = model.encode(
        pairs["Human Answer"].tolist(), normalize_embeddings=True, show_progress_bar=False
    )
    ai_embeddings = model.encode(
        pairs["AI Answer"].tolist(), normalize_embeddings=True, show_progress_bar=False
    )
    scores = (human_embeddings * ai_embeddings).sum(axis=1)
    result = pairs[["Person ID", "Question Category", "Question Text"]].copy()
    result.insert(0, "row_number", range(2, len(pairs) + 2))
    result["cosine_similarity"] = scores
    result["model_name"] = model_name
    return result


def add_bertscore(scores: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    try:
        from bert_score import score as bert_score
    except ImportError as error:
        raise RuntimeError("Install the required semantic dependencies with pip install -e .") from error

    precision, recall, f1 = bert_score(
        cands=pairs["AI Answer"].tolist(),
        refs=pairs["Human Answer"].tolist(),
        lang="en",
        verbose=False,
    )
    scores["bertscore_precision"] = precision.cpu().numpy()
    scores["bertscore_recall"] = recall.cpu().numpy()
    scores["bertscore_f1"] = f1.cpu().numpy()
    return scores


def add_rouge_l(scores: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    try:
        from rouge_score import rouge_scorer
    except ImportError as error:
        raise RuntimeError("Install the required semantic dependencies with pip install -e .") from error

    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    rouge_values = [
        scorer.score(human_answer, ai_answer)["rougeL"]
        for human_answer, ai_answer in zip(pairs["Human Answer"], pairs["AI Answer"])
    ]
    scores["rougeL_precision"] = [value.precision for value in rouge_values]
    scores["rougeL_recall"] = [value.recall for value in rouge_values]
    scores["rougeL_f1"] = [value.fmeasure for value in rouge_values]
    return scores


def summarize_scores(scores: pd.DataFrame) -> pd.DataFrame:
    metric_columns = [
        "cosine_similarity", "bertscore_precision", "bertscore_recall", "bertscore_f1",
        "rougeL_precision", "rougeL_recall", "rougeL_f1",
    ]
    summaries = []
    groups = [("overall", "all", scores)]
    groups.extend(
        ("question_category", category, group)
        for category, group in scores.groupby("Question Category", sort=True)
    )
    for group_type, group_name, group in groups:
        for metric in metric_columns:
            values = group[metric]
            summaries.append({
                "group_type": group_type,
                "group": group_name,
                "metric": metric,
                "count": int(values.count()),
                "mean": float(values.mean()),
                "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
                "min": float(values.min()),
                "25%": float(values.quantile(0.25)),
                "50%": float(values.quantile(0.50)),
                "75%": float(values.quantile(0.75)),
                "max": float(values.max()),
            })
    return pd.DataFrame(summaries)


def run(input_file: Path = INPUT_FILE, output_dir: Path = OUTPUT_DIR,
        model_name: str = DEFAULT_MODEL) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir.mkdir(parents=True, exist_ok=True)
    pairs = load_pairs(input_file)
    scores = embed_pairs(pairs, model_name=model_name)
    scores = add_bertscore(scores, pairs)
    scores = add_rouge_l(scores, pairs)
    summary = summarize_scores(scores)
    scores.to_csv(output_dir / "semantic_similarity_scores.csv", index=False)
    summary.to_csv(output_dir / "semantic_similarity_summary.csv", index=False)
    metadata = {
        "input_file": str(input_file),
        "model_name": model_name,
        "metrics": [
            "cosine similarity of L2-normalized sentence embeddings",
            "BERTScore precision, recall, and F1",
            "ROUGE-L precision, recall, and F1",
        ],
        "row_count": len(scores),
        "notes": [
            "Scores compare each human answer with the AI answer in the same workbook row.",
            "Cosine similarity is a semantic relatedness signal, not a factual or quality score.",
        ],
    }
    (output_dir / "semantic_similarity_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return scores, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT_FILE)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    scores, summary = run(args.input, args.output_dir, args.model)
    print(f"Scored {len(scores)} human/AI pairs with {args.model}.")
    print(summary[summary["group_type"] == "overall"].to_string(index=False))


if __name__ == "__main__":
    main()