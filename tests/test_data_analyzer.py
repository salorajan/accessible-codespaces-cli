"""Unit tests for CSV Analyzer and Imputation."""

import tempfile
import unittest
from pathlib import Path

from src.data_analyzer import CSVAnalyzer, is_missing, try_parse_float


class TestCSVAnalyzer(unittest.TestCase):
    """Test suite for missing value identification and imputation."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.sample_csv = Path(self.temp_dir.name) / "test_data.csv"
        
        # Write small sample CSV
        content = (
            "id,name,score,department\n"
            "1,Alice,90,Engineering\n"
            "2,Bob,,Marketing\n"
            "3,,85,Engineering\n"
            "4,Diana,NA,HR\n"
            "5,Evan,95,\n"
        )
        self.sample_csv.write_text(content, encoding="utf-8")
        self.analyzer = CSVAnalyzer(self.sample_csv)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_missing_token_detection(self) -> None:
        self.assertTrue(is_missing(""))
        self.assertTrue(is_missing("NA"))
        self.assertTrue(is_missing("NaN"))
        self.assertTrue(is_missing("null"))
        self.assertTrue(is_missing("?"))
        self.assertFalse(is_missing("Alice"))
        self.assertFalse(is_missing("123"))

    def test_try_parse_float(self) -> None:
        self.assertEqual(try_parse_float("42.5"), 42.5)
        self.assertEqual(try_parse_float("100"), 100.0)
        self.assertIsNone(try_parse_float("NA"))
        self.assertIsNone(try_parse_float("Engineering"))

    def test_analysis_stats(self) -> None:
        stats = self.analyzer.analyze_missing()
        self.assertEqual(self.analyzer.total_rows, 5)
        self.assertEqual(self.analyzer.total_columns, 4)

        # 'score' column has 2 missing (Bob, Diana) out of 5
        score_stat = stats["score"]
        self.assertEqual(score_stat["missing_count"], 2)
        self.assertEqual(score_stat["valid_count"], 3)
        self.assertEqual(score_stat["inferred_type"], "numeric")
        self.assertEqual(score_stat["mean"], 90.0)

        # 'department' column has 1 missing (Evan)
        dept_stat = stats["department"]
        self.assertEqual(dept_stat["missing_count"], 1)
        self.assertEqual(dept_stat["inferred_type"], "text")
        self.assertEqual(dept_stat["mode"], "Engineering")

    def test_imputation_auto(self) -> None:
        out_csv = Path(self.temp_dir.name) / "imputed.csv"
        imputed_rows, log = self.analyzer.impute(strategy="auto", output_filepath=out_csv)

        self.assertTrue(out_csv.exists())
        self.assertEqual(len(imputed_rows), 5)

        # Verify no missing cells remain
        re_analyzer = CSVAnalyzer(out_csv)
        re_stats = re_analyzer.analyze_missing()
        for col, s in re_stats.items():
            self.assertEqual(s["missing_count"], 0, f"Column {col} still has missing values")

    def test_accessible_summary_output(self) -> None:
        summary = self.analyzer.get_accessible_summary()
        self.assertIn("DATASET MISSING VALUE ANALYSIS REPORT", summary)
        self.assertIn("Total Rows: 5", summary)
        self.assertIn("Total Columns: 4", summary)
        self.assertIn("Column 3: score", summary)


if __name__ == "__main__":
    unittest.main()
