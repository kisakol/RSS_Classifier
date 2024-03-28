# RSS Classification

This package provides a function for RSS clasification. Paper: 


## Installation (pip)

To install the package, you can use `pip`:

```pip install git+https://github.com/kisakol/RSS_Classifier.git```


## Installation (Docker)
will be updated soon

## Args
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


### Using the Function

To use the function, simply import it and call it with the required arguments:

```python
from rssclassifier.rssmodel import rss_predict

# Prepare input data
dataframe_path = "path/to/df"

# Call the function
rss_predict(dataframe_path, output="RSS_classifications")
```

# Reference
Kisakol, B., Matveeva, A., Salvucci, M. et al. Identification of unique rectal cancer-specific subtypes. Br J Cancer (2024). https://doi.org/10.1038/s41416-024-02656-0
