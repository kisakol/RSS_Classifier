import unittest
from code.rssclassification import rssclassifier

class TestFunction(unittest.TestCase):
    def test_function(self):
        # Define paths (can be passed as arguments or retrieved from environment variables)

        model_path = "../data/model/model_XgBoost_Rectal_Specific_Classifier.json"
        modules_path = "../data/gene_modules/filtered_genes_modules.txt"
        output_path = "../output/RSSpredictions"
        dataframe_path = "../input/rectal182.txt"

        # Call the function with user-defined paths
        rssclassifier(dataframe_path, model_path, modules_path, scaled=False, output=output_path)


if __name__ == "__main__":
    unittest.main()