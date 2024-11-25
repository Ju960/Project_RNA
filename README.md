# Project_RNA

## Project Description

The goal of this project is to compute coarse-grained RMSD (Root Mean Square Deviation) and analyze its correlation with three existing metrics: 
- RMSD: Root Mean Square Deviation
- MCQ: Max Cluster Quality
- TM-Score: Template Modeling Score

The main question we aim to address is: 
Which coarse-grained representation has the highest correlation to current metrics?

## Objectives

1. Compute coarse-grained RMSD using a custom implementation.
2. Analyze correlation scores between coarse-grained RMSD and the metrics (RMSD, MCQ, TM-Score).

## Repository Structure
├──Data/ # Contains native structures, predicted structures and their scores according to basic metrics
├──custom_rmsd/ # Package to compute custom RMSD for different atom combinations and compare them to the basic metrics
├──README.md/ # This file

## Installation

Clone this repository and install the required dependencies:

```bash
git clone <https://github.com/Ju960/Project_RNA.git>
cd custom_rmsd
pip install -r requirements.txt
```

## Usage
See the package's README.md file

## Contributors

- Group Member 1: Julia GOUNIN
- Group Member 2: Océane SAIBOU
- Group Member 3: Reshma VASANTE 

