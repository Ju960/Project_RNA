# custom_rmsd

`custom_rmsd` is a Python package designed for coarse-grained RMSD (cgRMSD) calculations, correlation analysis between metrics, and visualization of results in the context of 3D structure prediction and evaluation, primarily for RNA molecules.

## Package structure

custom_rmsd/
├── [__init__.py](__init__.py)
├── [rmsd_calculation.py](rmsd_calculation.py)   # Functions for loading structures and compute custom RMSD values
├── [correlations.py](correlations.py)       # Functions to calculate correlations between basic metrics and cgRMSD values.
├── [visualizations.py](visualizations.py)    # Functions to create plots and correlation matrices
├── [scores_comparisons.py](scores_comparisons.py) # Functions for merging result files
├── [README.md](README.md) # This file
├── [requirements.txt](requirements.txt) # Required packages
├── [example.ipynb](../example.ipynb) # Use example
├──  [rmsd_1nat_1pred.py](rmsd_1nat_1pred.py)# Code to compute the custom RMSD calculation for 1 native and 1 prediction

## Installation

Clone this repository and install the required dependencies:

```bash
git clone <https://github.com/Ju960/Project_RNA.git>
cd custom_rmsd
pip install -r requirements.txt
```

## Usage

### RMSD calculation (cgRMSD)

To calculate the cgRMSD between a native structure and its predictions:

```python
from custom_rmsd.rmsd_calculation import process_native_prediction

native_path = "path/to/native.pdb"
pred_dir = "path/to/predictions/"
score_file = "path/to/scores.csv"
atom_combinations = [["list of atom combination for cgRMSD"], ["list of atom combination for cgRMSD"]]  # Atom combinations to use

process_native_prediction(native_path, pred_dir, score_file, atom_combinations)
```

To calculate the cgRMSD between a set of native structure and their predictions:

```python
from custom_rmsd.rmsd_calculation import process_native_prediction

native_dir = "path/to/native_directory/"
pred_dir = "path/to/predictions/"
score_dir = "path/to/score_directory"
atom_combinations = [["list of atom combination for cgRMSD"], ["list of atom combination for cgRMSD"]]  # Atom combinations to use

process_all_natives(native_dir, pred_dir, score_dir, atom_combinations)
```

### Correlation analysis

To calculate correlations between all metrics in a directory containing the generated CSV files:

```python
from custom_rmsd.correlations import create_correlation_matrix

csv_dir = "path/to/csv_files/"
output_file = "correlations.csv"
create_correlation_matrix(csv_dir, output_file, method="spearman")  # or "pearson"
```

### Correlation Visualization

To create a correlation matrix plot and save it as an image:

```python
from custom_rmsd.visualizations import plot_correlation_matrix

correlation_file = "correlations.csv"
output_image = "correlation_matrix.png"
plot_correlation_matrix(correlation_file, output_image)
```

### Score comparison

```python
from custom_rmsd.score_comparison import concat_files
from custom_rmsd.visualizations import plot_metrics_vs_cgRMSD

score_dir = "path/to/score_dir/"
all_scores_file = "concatenated_results.csv"
output_folder = "path/to/output_folder/"

concat_files(score_dir, all_scores_file)
plot_metrics_vs_cgRMSD(all_scores_file, output_folder)
```

## Examples

Detailed usage examples can be found in the [example.ipynb](../example.ipynb) file

## Authors

Océane SAÏBOU - M2 GENIOMHE University of Evry
Julia GOUNIN - M2 GENIOMHE University of Evry
Reshma VASANTE - M2 GENIOMHE University of Evry

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
