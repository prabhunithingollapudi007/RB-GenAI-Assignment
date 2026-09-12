import unittest
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from rb_genai_analysis.pipeline import normalize_text, response_metrics
from rb_genai_analysis.semantic_analysis import load_pairs, summarize_scores


PROCESSED = PROJECT_ROOT / "data" / "processed"


class PipelineTests(unittest.TestCase):
    def test_normalize_text_collapses_whitespace(self):
        self.assertEqual(normalize_text("  one\n two  "), "one two")

    def test_response_metrics_calculates_core_fields(self):
        metrics = response_metrics("A convenient product with a good price")
        self.assertEqual(metrics["word_count"], 7)
        self.assertEqual(metrics["unique_word_count"], 6)
        self.assertTrue(metrics["has_concrete_language"])
        self.assertTrue(metrics["has_abstract_language"])

    def test_processed_paired_table_has_expected_schema(self):
        pairs = load_pairs(PROCESSED / "paired_answers_clean.csv")
        self.assertEqual(len(pairs), 30)
        self.assertEqual(
            list(pairs.columns),
            ["Person ID", "Question Category", "Question Text", "Human Answer", "AI Answer"],
        )

    def test_semantic_summary_contains_all_required_metrics(self):
        scores = pd.read_csv(PROCESSED / "semantic_similarity_scores.csv")
        summary = summarize_scores(scores)
        required_metrics = {
            "cosine_similarity", "bertscore_precision", "bertscore_recall", "bertscore_f1",
            "rougeL_precision", "rougeL_recall", "rougeL_f1",
        }
        self.assertEqual(set(summary["metric"]), required_metrics)
        self.assertEqual(len(scores), 30)


if __name__ == "__main__":
    unittest.main()