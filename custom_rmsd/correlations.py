import os
import pandas as pd
from scipy.stats import spearmanr, pearsonr
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

def compute_correlations(score_dir):
    """
    Computes correlation coefficients between coarse-grained RMSD and reference metrics.
    :param score_dir: Directory containing CSV score files
    :return: Aggregated correlation results
    """
    all_correlations = []
    for score_file in os.listdir(score_dir):
        if score_file.endswith(".csv"):
            df = pd.read_csv(os.path.join(score_dir, score_file))
            for combination in ATOM_COMBINATIONS:
                col_name = f"RMSD_{'_'.join(combination)}"
                if col_name not in df.columns:
                    continue
                for metric in ["RMSD", "MCQ", "TM-Score"]:
                    if metric not in df.columns:
                        continue
                    spearman_corr, _ = spearmanr(df[metric], df[col_name], nan_policy='omit')
                    pearson_corr, _ = pearsonr(df[metric], df[col_name])
                    all_correlations.append((score_file, combination, metric, spearman_corr, pearson_corr))
    
    result_df = pd.DataFrame(all_correlations, columns=["File", "Combination", "Metric", "Spearman", "Pearson"])
    return result_df

