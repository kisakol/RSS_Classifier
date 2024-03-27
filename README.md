# RSS Classification

This package provides a function for RSS clasification. Paper: 


## Installation (pip)

To install the package, you can use `pip`:

```pip install git+https://github.com/kisakol/RSS_Classifier.git```


## Installation (Docker)
```docker pull yourusername/yourimage:tag```
```docker build -t my_package .```

## Args
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


### Using the Function

To use the function, simply import it and call it with the required arguments:

```python
import pandas as pd
from rss_classification import RSS_Classifier

# Prepare input data
df_to = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
model_path = "path/to/model.json"
modules_path = "path/to/modules"

# Call the function
RSS_Classifier(df_to, model_path, modules_path, scaled=False, output="RSS_classifications")
```

# Reference
Kisakol, B., Matveeva, A., Salvucci, M. et al. Identification of unique rectal cancer-specific subtypes. Br J Cancer (2024). https://doi.org/10.1038/s41416-024-02656-0