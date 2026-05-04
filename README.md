# RSS Classifier

An XGBoost-based classifier for predicting **Rectal-cancer Specific Subtypes (RSS1/2/3)** from log2-normalised gene expression data.

> **Reference:** Kisakol, B., Matveeva, A., Salvucci, M. et al. *Identification of unique rectal cancer-specific subtypes.* Br J Cancer (2024). https://doi.org/10.1038/s41416-024-02656-0

## Input Format

Rows = samples, Columns = genes (HUGO symbols). Values must be **log2-transformed** gene expression counts.

```
        GENE1   GENE2   GENE3   ...
SAMPLE1  5.12   3.87    6.20   ...
SAMPLE2  4.90   4.10    5.88   ...
```

See `input/rectal182.txt` for a full example.


---

## How It Works

1. Gene expression values are z-score scaled (unless `--scaled` is provided).
2. Genes are grouped into pre-defined modules (`data/gene_modules/filtered_genes_modules.txt`); each module is summarised by its median expression.
3. The pre-trained XGBoost model predicts one of three subtypes — **RSS1**, **RSS2**, or **RSS3** per sample.
4. Results are written to a tab-separated `.txt` file.

---


## Installation

### Option 1: pip

```bash
pip install git+https://github.com/kisakol/RSS_Classifier.git
```

### Option 2: conda / mamba

> [mamba](https://mamba.readthedocs.io) is a faster drop-in replacement for conda. Either works below.

```bash
# 1. Clone the repository
git clone https://github.com/kisakol/RSS_Classifier.git
cd RSS_Classifier

# 2. Create the environment from the provided spec
conda env create -f environment/environment.yml
# or, with mamba:
mamba env create -f environment/environment.yml

# 3. Activate it
conda activate rssclassifier
# or, with mamba
mamba activate rssclassifier

# 4. Install the package in editable mode
pip install -e .
```

To update the environment later:
```bash
conda env update -f environment/environment.yml --prune
```

To export your current environment for sharing:
```bash
conda env export --no-builds > environment/environment.yml
```

### Option 3: Docker

```bash
# 1. Clone the repository
git clone https://github.com/kisakol/RSS_Classifier.git
cd RSS_Classifier

# 2. Build the image
docker build -f environment/Dockerfile -t rssclassifier .

# 3. Run the classifier (mount your data directory)
docker run --rm \
  -v "$(pwd)/input":/input \
  -v "$(pwd)/output":/output \
  rssclassifier \
  python -m rssclassifier.rssmodel_cmd \
    --dataframe_path /input/rectal182.txt \
    --output /output/RSS_predictions
```

---

## Usage

### As a Python library

```python
from rssclassifier.rssmodel import rss_predict

rss_predict(
    dataframe_path="input/rectal182.txt",
    scaled=False,              # set True if your data is already z-score scaled
    output="output/RSS_predictions",
)
```

### From the command line

```bash
python -m rssclassifier.rssmodel_cmd \
    --dataframe_path input/rectal182.txt \
    --output output/RSS_predictions
```

### Optional arguments

| Argument | Default | Description |
|---|---|---|
| `--dataframe_path` | *(required)* | Path to the input TSV (samples × genes) |
| `--model` | bundled `.json` | Path to an alternative model file |
| `--modules` | bundled `.txt` | Path to an alternative gene-modules file |
| `--scaled` | `False` | Pass `True` if data are already z-score scaled |
| `--output` | `RSS_predictions` | Output file prefix (`.txt` is appended) |

### Output

A tab-separated file with two columns:

```
        RSS
SAMPLE1 RSS1
SAMPLE2 RSS3
SAMPLE3 RSS2
```

---

## Running Tests

```bash
cd test
python -m unittest test.py
```

---

## Project Structure

```
RSS_Classifier/
├── data/
│   ├── gene_modules/       # Gene-to-module mapping
│   └── model/              # Pre-trained XGBoost model (JSON + joblib)
├── environment/
│   ├── Dockerfile          # Docker build file
│   └── environment.yml     # Conda/mamba environment spec
├── input/                  # Example input (rectal182.txt)
├── output/                 # Example output
├── rssclassifier/
│   ├── rssmodel.py         # Core rss_predict() function
│   └── rssmodel_cmd.py     # CLI entry point
├── test/
│   └── test.py
└── setup.py
```
