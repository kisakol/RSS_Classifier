import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import os

def rssclassifier(
    dataframe_path: str,
    model_path: str = "../data/model/model_XgBoost_Rectal_Specific_Classifier.json",
    modules_path: str = "../data/gene_modules/filtered_genes_modules.txt",
    scaled: bool = False,
    output: str = "RSS_predictions",
) -> None:
    
    """
    Predicts the RSS clusters of the input data using the trained model and gene modules.
    Args:
        dataframe_path: The input data path. Rows should be samples and columns should be genes. First row should be the gene names (HUGO SYMBOLS). Data should be log2 transformed.
        model_path: str: The path to the trained model.
        modules_path: str: The path to the modules file.
        scaled: bool: If the input data is scaled. Default is False.
        output: str: The output file name. Default is "RSS_predictions".
    Returns:
        None
    Writes:
        A file with the predicted RSS clusters.
    """
    
    model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'model', 'model_XgBoost_Rectal_Specific_Classifier.json')
    modules_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'gene_modules', 'filtered_genes_modules.txt')
    
    print(os.getcwd())


    clf = XGBClassifier()
    clf.load_model(model_path)

    df = pd.read_csv(dataframe_path, sep="\t", index_col=0)

    genes_modules = pd.read_csv(modules_path, sep="\t")
    genes_modules.columns = ["genes", "modules"]
    groups_filtered_df = genes_modules.set_index("genes")

    if scaled:
        median_module = df.copy()
    else:
        scaler = StandardScaler()
        median_module = scaler.fit_transform(df)

    median_module = pd.DataFrame(median_module, index=df.index, columns=df.columns)

    median_module = (
        pd.merge(
            median_module[
                list(set(median_module.columns) & set(groups_filtered_df.index))
            ].T,
            groups_filtered_df,
            left_index=True,
            right_index=True,
        )
        .groupby("modules")
        .median()
        .T
    )

    median_module = median_module.drop("0", axis=1)

    predicted_labels = clf.predict(median_module)

    clusters2 = pd.DataFrame(
        predicted_labels, index=median_module.index, columns=["RSS"]
    )

    clusters2.RSS.replace({"C1": "RSS1", "C2": "RSS2", "C3": "RSS3"}, inplace=True)

    clusters2.to_csv("{out}.txt".format(out=output), sep="\t")