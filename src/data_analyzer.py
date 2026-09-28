"""Data analyzer core module for CSV inspection and missing value imputation.

Designed for high accessibility, robust execution without external C-extensions,
and clear human/screen-reader friendly diagnostic summaries.
"""

from __future__ import annotations

import csv
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

MISSING_TOKENS = {"", "na", "n/a", "nan", "null", "none", "?", "missing", "."}


def is_missing(value: Any) -> bool:
    """Determine whether a given cell value is considered missing."""
    if value is None:
        return True
    str_val = str(value).strip().lower()
    return str_val in MISSING_TOKENS


def try_parse_float(value: Any) -> Optional[float]:
    """Attempt to parse a value as float; return None if missing or not numerical."""
    if is_missing(value):
        return None
    try:
        val = float(str(value).strip())
        if math.isnan(val):
            return None
        return val
    except ValueError:
        return None


class CSVAnalyzer:
    """Analyzes CSV tabular datasets and handles missing value replacements."""

    def __init__(self, filepath: Union[str, Path]) -> None:
        self.filepath = Path(filepath)
        self.headers: List[str] = []
        self.rows: List[List[str]] = []
        self._load()

    def _load(self) -> None:
        """Load CSV data from disk into memory."""
        if not self.filepath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filepath}")

        with open(self.filepath, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            try:
                self.headers = [h.strip() for h in next(reader)]
            except StopIteration:
                self.headers = []
                self.rows = []
                return

            self.rows = [[cell.strip() for cell in row] for row in reader]

    @property
    def total_rows(self) -> int:
        """Return total number of data rows."""
        return len(self.rows)

    @property
    def total_columns(self) -> int:
        """Return total number of columns."""
        return len(self.headers)

    def analyze_missing(self) -> Dict[str, Dict[str, Any]]:
        """Compute detailed missing value statistics per column."""
        results: Dict[str, Dict[str, Any]] = {}
        total = self.total_rows

        for col_idx, header in enumerate(self.headers):
            values = [row[col_idx] if col_idx < len(row) else "" for row in self.rows]
            missing_count = sum(1 for v in values if is_missing(v))
            valid_values = [v for v in values if not is_missing(v)]
            
            # Infer column type
            numeric_parsed = [try_parse_float(v) for v in valid_values]
            is_numeric = len(valid_values) > 0 and all(n is not None for n in numeric_parsed)

            missing_pct = (missing_count / total * 100.0) if total > 0 else 0.0

            stats: Dict[str, Any] = {
                "header": header,
                "total_count": total,
                "valid_count": len(valid_values),
                "missing_count": missing_count,
                "missing_pct": round(missing_pct, 2),
                "inferred_type": "numeric" if is_numeric else "text",
            }

            if is_numeric and valid_values:
                nums = [n for n in numeric_parsed if n is not None]
                stats["min"] = min(nums)
                stats["max"] = max(nums)
                stats["mean"] = round(statistics.mean(nums), 2)
                stats["median"] = round(statistics.median(nums), 2)
            elif valid_values:
                counter = Counter(valid_values)
                most_common = counter.most_common(1)
                stats["mode"] = most_common[0][0] if most_common else None
                stats["unique_count"] = len(counter)

            results[header] = stats

        return results

    def impute(
        self,
        strategy: str = "auto",
        custom_strategies: Optional[Dict[str, str]] = None,
        output_filepath: Optional[Union[str, Path]] = None,
    ) -> Tuple[List[List[str]], Dict[str, Any]]:
        """Impute missing values across all columns.
        
        Supported strategies:
          - 'auto': Mean for numeric columns, Mode for text columns.
          - 'mean': Mean for all numeric columns.
          - 'median': Median for all numeric columns.
          - 'mode': Most frequent value for all columns.
          - 'zero_or_unknown': 0 for numeric, 'Unknown' for text.
        """
        analysis = self.analyze_missing()
        custom_strategies = custom_strategies or {}
        imputed_rows: List[List[str]] = []
        imputation_log: Dict[str, Any] = {}

        # Precompute replacement values per column
        replacements: Dict[str, str] = {}
        for header, stat in analysis.items():
            strat = custom_strategies.get(header, strategy)
            col_type = stat["inferred_type"]

            if stat["missing_count"] == 0:
                replacements[header] = ""
                imputation_log[header] = {"imputed": 0, "strategy": "none"}
                continue

            if strat == "auto":
                strat = "mean" if col_type == "numeric" else "mode"

            if strat == "mean" and col_type == "numeric":
                val_str = str(stat.get("mean", 0))
            elif strat == "median" and col_type == "numeric":
                val_str = str(stat.get("median", 0))
            elif strat == "mode":
                val_str = str(stat.get("mode", "Unknown"))
            elif strat == "zero_or_unknown":
                val_str = "0" if col_type == "numeric" else "Unknown"
            else:
                # Fallback or literal constant value
                val_str = strat

            replacements[header] = val_str
            imputation_log[header] = {
                "imputed_count": stat["missing_count"],
                "strategy": strat,
                "replacement_value": val_str,
            }

        # Generate transformed dataset
        for row in self.rows:
            new_row: List[str] = []
            for col_idx, header in enumerate(self.headers):
                val = row[col_idx] if col_idx < len(row) else ""
                if is_missing(val):
                    new_row.append(replacements[header])
                else:
                    new_row.append(val)
            imputed_rows.append(new_row)

        if output_filepath:
            out_path = Path(output_filepath)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
                writer.writerows(imputed_rows)

        return imputed_rows, imputation_log

    def get_accessible_summary(self) -> str:
        """Produce a clean, screen-reader friendly text summary of the analysis."""
        stats = self.analyze_missing()
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("DATASET MISSING VALUE ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append(f"Source File: {self.filepath.name}")
        lines.append(f"Total Rows: {self.total_rows}")
        lines.append(f"Total Columns: {self.total_columns}")
        lines.append("-" * 60)

        total_missing_cells = sum(s["missing_count"] for s in stats.values())
        total_cells = self.total_rows * self.total_columns if self.total_rows > 0 else 1
        overall_missing_pct = round((total_missing_cells / total_cells) * 100.0, 2)
        lines.append(f"Total Missing Cells: {total_missing_cells} out of {total_cells} ({overall_missing_pct}%)")
        lines.append("-" * 60)
        lines.append("Column Details:")

        for idx, (header, s) in enumerate(stats.items(), start=1):
            lines.append(f"Column {idx}: {header}")
            lines.append(f"  Type: {s['inferred_type']}")
            lines.append(f"  Missing: {s['missing_count']} of {s['total_count']} rows ({s['missing_pct']}%)")
            if s['inferred_type'] == 'numeric' and s.get('mean') is not None:
                lines.append(f"  Mean: {s['mean']}, Median: {s['median']}, Range: [{s['min']} to {s['max']}]")
            elif s.get('mode') is not None:
                lines.append(f"  Most Frequent (Mode): '{s['mode']}', Unique Values: {s.get('unique_count')}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)
