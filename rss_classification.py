import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler

def predict_rss(df_to: pd.DataFrame, model_path: str, modules_path: str, scaled: bool = False, output: str = "RSS_predictions") -> None:
    
    clf = XGBClassifier()
    clf.load_model(model_path)
    
    genes_m = pd.read_csv(modules_path, sep="\t")
    genes_m.columns = ["genes", "modules"]
    groups_filtered_df = genes_m.set_index("genes")
    
    if scaled:
        module_median2 = df_to.copy()
    else:
        scaler = StandardScaler()
        module_median2 = scaler.fit_transform(df_to)

    module_median2 = pd.DataFrame(module_median2, index=df_to.index, columns=df_to.columns)

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
        predicted_labels, index=module_median2.index, columns=["HClusters"]
    )

    clusters2.to_csv("{out}.txt".format(out=output), sep="\t")