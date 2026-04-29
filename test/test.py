import os
import unittest
from rssclassifier.rssmodel import rss_predict

# Resolve paths relative to the test file so tests work from any working directory
_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_DIR = os.path.join(_TEST_DIR, "..")


class TestRssPredict(unittest.TestCase):
    def test_predict_runs_and_produces_output(self):
        dataframe_path = os.path.join(_REPO_DIR, "input", "rectal182.txt")
        output_path = os.path.join(_REPO_DIR, "output", "RSS_predictions_test")

        rss_predict(
            dataframe_path=dataframe_path,
            scaled=False,
            output=output_path,
        )

        result_file = f"{output_path}.txt"
        self.assertTrue(
            os.path.isfile(result_file),
            f"Expected output file not found: {result_file}",
        )

        import pandas as pd
        results = pd.read_csv(result_file, sep="\t", index_col=0)
        self.assertIn("RSS", results.columns)
        self.assertTrue(len(results) > 0, "Output file is empty.")
        self.assertTrue(
            results["RSS"].isin(["RSS1", "RSS2", "RSS3"]).all(),
            f"Unexpected labels found: {results['RSS'].unique()}",
        )


if __name__ == "__main__":
    unittest.main()
