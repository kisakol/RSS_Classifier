"""
Command-line entry point for the RSS Classifier.

Usage:
    python -m rssclassifier.rssmodel_cmd --dataframe_path input/rectal182.txt
    python -m rssclassifier.rssmodel_cmd --dataframe_path input/rectal182.txt \\
        --output output/RSS_predictions --scaled
"""

import argparse
from rssclassifier.rssmodel import rss_predict, _DEFAULT_MODEL, _DEFAULT_MODULES


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run RSS classification on gene expression data."
    )
    parser.add_argument(
        "--dataframe_path",
        required=True,
        help="Path to the input TSV (samples × genes, log2-transformed).",
    )
    parser.add_argument(
        "--model",
        default=_DEFAULT_MODEL,
        help="Path to the XGBoost model file (.json). Defaults to bundled model.",
    )
    parser.add_argument(
        "--modules",
        default=_DEFAULT_MODULES,
        help="Path to the gene-modules file (.txt). Defaults to bundled file.",
    )
    parser.add_argument(
        "--scaled",
        action="store_true",          # flag: present = True, absent = False
        help="Pass this flag if the input data is already z-score scaled.",
    )
    parser.add_argument(
        "--output",
        default="RSS_predictions",
        help="Output file prefix (.txt will be appended). Default: RSS_predictions.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    rss_predict(
        dataframe_path=args.dataframe_path,
        model_path=args.model,
        modules_path=args.modules,
        scaled=args.scaled,
        output=args.output,
    )
