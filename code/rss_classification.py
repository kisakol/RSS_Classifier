import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

def RSSClassifier(df: pd.DataFrame, model_path: str = "../data/model/model_XgBoost_Rectal_Specific_Classifier.json",
                 modules_path: str = "../data/gene_modules/filtered_genes_modules.txt", 
                 scaled: bool = False, output: str = "RSS_predictions") -> None:

    """
    Predicts the RSS clusters of the input data using the trained model and gene modules.  
    Args:  
        df: pd.DataFrame: The input data.  Rows should be samples and columns should be genes. First row should be the gene names (HUGO SYMBOLS). Data should be log2 transformed.
        model_path: str: The path to the trained model.  
        modules_path: str: The path to the modules file.  
        scaled: bool: If the input data is scaled. Default is False.  
        output: str: The output file name. Default is "RSS_predictions".
    Returns:
        None
    Writes:
        A file with the predicted RSS clusters. 
    """
    
    clf = XGBClassifier()
    clf.load_model(model_path)
    
    genes_m = pd.read_csv(modules_path, sep="\t")
    genes_m.columns = ["genes", "modules"]
    groups_filtered_df = genes_m.set_index("genes")
    
    if scaled:
        module_median2 = df.copy()
    else:
        scaler = StandardScaler()
        module_median2 = scaler.fit_transform(df)

    module_median2 = pd.DataFrame(module_median2, index=df.index, columns=df.columns)

    module_median2 = (
        pd.merge(
            module_median2[
                list(set(module_median2.columns) & set(groups_filtered_df.index))
            ].T,
            groups_filtered_df,
            left_index=True,
            right_index=True,
        )
        .groupby("modules")
        .median()
        .T
    )

    module_median2 = module_median2.drop("0", axis=1)

    predicted_labels = clf.predict(module_median2)

    clusters2 = pd.DataFrame(
        predicted_labels, index=module_median2.index, columns=["RSS"]
    )
    
    clusters2.RSS.replace({"C1": "RSS1", "C2": "RSS2", "C3": "RSS3"}, inplace=True)

    clusters2.to_csv("{out}.txt".format(out=output), sep="\t")