import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier



_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_MODEL = os.path.join(_PKG_DIR, "..", "data", "model",
                              "model_XgBoost_Rectal_Specific_Classifier.json")
_DEFAULT_MODULES = os.path.join(_PKG_DIR, "..", "data", "gene_modules",
                                "filtered_genes_modules.txt")


def rss_predict(
    dataframe_path: str,
    model_path: str = _DEFAULT_MODEL,
    modules_path: str = _DEFAULT_MODULES,
    scaled: bool = False,
    output: str = "RSS_predictions",
) -> None:
    """
    Predict RSS clusters for samples using the pre-trained XGBoost model.

    Args:
        dataframe_path: Path to the input TSV. Rows = samples, columns = genes
            (HUGO symbols). Values must be log2-transformed.
        model_path:    Path to the trained XGBoost model (.json). Defaults to
                       the bundled model inside the package.
        modules_path:  Path to the gene-modules file (.txt, tab-separated,
                       columns: genes, modules). Defaults to the bundled file.
        scaled:        If True, skip z-score scaling (data already scaled).
                       Default is False.
        output:        Output file prefix. A '.txt' extension is appended.
                       Default is 'RSS_predictions'.

    Writes:
        A tab-separated file <output>.txt with columns [sample_id, RSS].
    """
    # --- Load model ---
    clf = XGBClassifier()
    clf.load_model(model_path)

    # --- Load expression data ---
    df = pd.read_csv(dataframe_path, sep="\t", index_col=0)

    # --- Load gene modules ---
    genes_modules = pd.read_csv(modules_path, sep="\t", header=None,
                                names=["genes", "modules"])
    groups_filtered_df = genes_modules.set_index("genes")

    # --- Scale (unless the caller says the data is already scaled) ---
    if scaled:
        scaled_df = df.copy()
    else:
        scaler = StandardScaler()
        scaled_values = scaler.fit_transform(df)
        scaled_df = pd.DataFrame(scaled_values, index=df.index, columns=df.columns)

    # --- Compute per-module medians ---
    common_genes = list(set(scaled_df.columns) & set(groups_filtered_df.index))
    if not common_genes:
        raise ValueError(
            "No overlap between the input gene names and the module gene list. "
            "Check that columns are HUGO symbols and data is not transposed."
        )

    median_module = (
        pd.merge(
            scaled_df[common_genes].T,
            groups_filtered_df,
            left_index=True,
            right_index=True,
        )
        .groupby("modules")
        .median()
        .T
    )

    # Drop module '0' if present
    if "0" in median_module.columns:
        median_module = median_module.drop("0", axis=1)

    # --- Predict ---
    predicted_labels = clf.predict(median_module)

    clusters = pd.DataFrame(
        predicted_labels, index=median_module.index, columns=["RSS"]
    )
    clusters["RSS"].replace(
        {"C1": "RSS1", "C2": "RSS2", "C3": "RSS3"}, inplace=True
    )

    out_path = f"{output}.txt"
    clusters.to_csv(out_path, sep="\t")
    print(f"Predictions written to: {out_path}")
