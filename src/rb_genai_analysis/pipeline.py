from pathlib import Path
import json
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET_FILE = PROJECT_ROOT / "data" / "raw" / "RB_GenAI_Datatest.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)?")
CONCRETE_TERMS = {
    "brand", "brands", "product", "products", "skincare", "sunscreen", "shampoo",
    "supermarket", "store", "stores", "drugstore", "instagram", "packaging", "price",
    "prices", "ingredient", "ingredients", "scent", "texture", "sample", "samples",
    "size", "sizes", "design", "budget", "friends", "reviews", "online",
}
ABSTRACT_TERMS = {
    "convenience", "convenient", "flexibility", "quality", "trust", "reliable", "reliability",
    "performance", "loyalty", "value", "values", "transparency", "confidence", "confidence",
    "sustainability", "sustainable", "effectiveness", "effective", "needs", "preference",
    "preferences", "reputation", "decision", "decisions", "influence", "influenced",
}
LIFESTYLE_TERMS = {
    "travel": r"\btravel(?:ing|led)?\b",
    "time": r"\btime\b|time[- ]efficient|saving time",
    "stress": r"\bstress(?:ed|ful)?\b",
    "professional_image": r"professional image|work image|appearance at work|look professional",
}


def normalize_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def word_tokens(value):
    return [token.lower() for token in WORD_PATTERN.findall(value)]


def response_metrics(value):
    text = normalize_text(value)
    tokens = word_tokens(text)
    unique_tokens = set(tokens)
    concrete_count = sum(token in CONCRETE_TERMS for token in tokens)
    abstract_count = sum(token in ABSTRACT_TERMS for token in tokens)
    metrics = {
        "word_count": len(tokens),
        "character_count": len(text),
        "unique_word_count": len(unique_tokens),
        "lexical_diversity": len(unique_tokens) / len(tokens) if tokens else 0.0,
        "concrete_term_count": concrete_count,
        "abstract_term_count": abstract_count,
        "has_concrete_language": concrete_count > 0,
        "has_abstract_language": abstract_count > 0,
    }
    for label, pattern in LIFESTYLE_TERMS.items():
        metrics[f"mentions_{label}"] = bool(re.search(pattern, text, flags=re.IGNORECASE))
    return metrics


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    xls = pd.ExcelFile(TARGET_FILE)
    raw = pd.read_excel(TARGET_FILE, sheet_name="answer_pairs")
    expected_columns = {
        "id", "question_category", "question", "person_id", "human_answers", "ai_answers"
    }
    missing_columns = expected_columns.difference(raw.columns)
    if missing_columns:
        raise ValueError(f"Missing expected columns: {sorted(missing_columns)}")

    paired = raw.rename(columns={
        "person_id": "Person ID",
        "question_category": "Question Category",
        "question": "Question Text",
        "human_answers": "Human Answer",
        "ai_answers": "AI Answer",
    })[["Person ID", "Question Category", "Question Text", "Human Answer", "AI Answer"]].copy()
    for column in paired.columns:
        paired[column] = paired[column].map(normalize_text)
    paired.to_csv(OUTPUT_DIR / "paired_answers_clean.csv", index=False, encoding="utf-8-sig")

    response_rows = []
    for row_number, row in paired.iterrows():
        for response_type in ("Human", "AI"):
            response = row[f"{response_type} Answer"]
            response_rows.append({
                "row_number": row_number + 2,
                "Person ID": row["Person ID"],
                "Question Category": row["Question Category"],
                "response_type": response_type,
                **response_metrics(response),
            })
    response_stats = pd.DataFrame(response_rows)
    response_stats.to_csv(OUTPUT_DIR / "response_level_metrics.csv", index=False)

    summaries = []
    for response_type, group in response_stats.groupby("response_type", sort=False):
        for metric in ("word_count", "character_count", "unique_word_count", "lexical_diversity",
                       "concrete_term_count", "abstract_term_count"):
            values = group[metric]
            summaries.append({
                "response_type": response_type,
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
    pd.DataFrame(summaries).to_csv(OUTPUT_DIR / "response_statistics.csv", index=False)

    presence_metrics = [column for column in response_stats.columns
                        if column.startswith("has_") or column.startswith("mentions_")]
    presence = []
    for response_type, group in response_stats.groupby("response_type", sort=False):
        for metric in presence_metrics:
            presence.append({
                "response_type": response_type,
                "metric": metric,
                "count": int(group[metric].sum()),
                "percent": float(group[metric].mean() * 100),
            })
    pd.DataFrame(presence).to_csv(OUTPUT_DIR / "language_presence_statistics.csv", index=False)

    missingness = []
    for column in paired.columns:
        missing_count = int(paired[column].eq("").sum())
        missingness.append({
            "field": column,
            "missing_count": missing_count,
            "missing_percent": missing_count / len(paired) * 100,
            "unique_count": int(paired[column].nunique(dropna=False)),
        })
    pd.DataFrame(missingness).to_csv(OUTPUT_DIR / "missingness_report.csv", index=False)

    artifacts = []
    for index, row in paired.iterrows():
        for response_type, raw_column in (("Human", "human_answers"), ("AI", "ai_answers")):
            text = row[f"{response_type} Answer"]
            raw_text = "" if pd.isna(raw.iloc[index][raw_column]) else str(raw.iloc[index][raw_column])
            if any(ord(character) > 127 for character in text):
                artifacts.append({"row_number": index + 2, "response_type": response_type,
                                  "artifact": "non_ascii_characters",
                                  "detail": "".join(sorted({character for character in text if ord(character) > 127}))})
            if re.search(r"\s{2,}", raw_text):
                artifacts.append({"row_number": index + 2, "response_type": response_type,
                                  "artifact": "repeated_whitespace", "detail": "multiple spaces"})
    for response_type, group in response_stats.groupby("response_type", sort=False):
        upper_bound = group["word_count"].quantile(0.75) + 1.5 * (
            group["word_count"].quantile(0.75) - group["word_count"].quantile(0.25)
        )
        for _, row in group[group["word_count"] > upper_bound].iterrows():
            artifacts.append({"row_number": int(row["row_number"]), "response_type": response_type,
                              "artifact": "unusually_long_response",
                              "detail": f"{int(row['word_count'])} words; threshold {upper_bound:.1f}"})
    pd.DataFrame(artifacts, columns=["row_number", "response_type", "artifact", "detail"]).to_csv(
        OUTPUT_DIR / "quality_artifacts_report.csv", index=False
    )

    metadata = {
        "source_file": TARGET_FILE.name,
        "sheet_names": xls.sheet_names,
        "sheet_used": "answer_pairs",
        "raw_shape": list(raw.shape),
        "paired_shape": list(paired.shape),
        "raw_columns": raw.columns.tolist(),
        "artifact_count": len(artifacts),
        "notes": [
            "Concrete and abstract language counts use transparent, small lexicons and are heuristic.",
            "Raw workbook values are preserved in the source workbook; clean outputs normalize whitespace only.",
        ],
    }
    (OUTPUT_DIR / "analysis_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Loaded {len(raw)} rows from {TARGET_FILE.name}, sheet 'answer_pairs'.")
    print(f"Wrote paired_answers_clean.csv and {len(artifacts)} quality flags.")
    print(response_stats.groupby("response_type")["word_count"].agg(["count", "mean", "median", "min", "max"]))


if __name__ == "__main__":
    main()