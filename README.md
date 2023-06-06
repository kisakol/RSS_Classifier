# RSS Classification
```
import rss_classification
predict_rss(df, "model/model_XgBoost_Rectal_Specific_Classifier.json", "gene_modules/filtered_genes_modules.txt")
```
run the code above to get RSS classifications. Dataframe format must be: Rows-Patients, Columns-Gene (Hugo Symbols)
