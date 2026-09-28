"""Command-Line Interface for Accessible CSV Data Analysis & Imputation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.data_analyzer import CSVAnalyzer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Accessible Terminal CSV Missing Value Analyzer and Imputer",
        epilog="Designed for high accessibility and terminal-first workflows in GitHub Codespaces."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="data/sample_data.csv",
        help="Path to the input CSV file (default: data/sample_data.csv)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="data/cleaned_data.csv",
        help="Path to export the cleaned CSV dataset (default: data/cleaned_data.csv)"
    )
    parser.add_argument(
        "-s", "--strategy",
        type=str,
        choices=["auto", "mean", "median", "mode", "zero_or_unknown"],
        default="auto",
        help="Imputation strategy: 'auto' (mean for numbers, mode for text), 'mean', 'median', 'mode', or 'zero_or_unknown'"
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Run analysis only without writing cleaned output file"
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' does not exist.", file=sys.stderr)
        return 1

    try:
        analyzer = CSVAnalyzer(input_path)
        print(analyzer.get_accessible_summary())

        if not args.analyze_only:
            output_path = Path(args.output)
            imputed_rows, log = analyzer.impute(
                strategy=args.strategy,
                output_filepath=output_path
            )
            print("=" * 60)
            print("IMPUTATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"Cleaned dataset saved to: {output_path.resolve()}")
            print("Imputation Actions Taken:")
            for header, details in log.items():
                if details.get("imputed_count", 0) > 0:
                    print(
                        f" - Column '{header}': Imputed {details['imputed_count']} missing cell(s) "
                        f"using '{details['strategy']}' strategy (Value: {details['replacement_value']})"
                    )
            print("=" * 60)

        return 0

    except Exception as exc:
        print(f"Fatal error during processing: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
