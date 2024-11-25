import os
import pandas as pd
from scipy.stats import spearmanr, pearsonr
import numpy as np
from itertools import combinations

def calculate_correlations(csv_dir, output_file, method="spearman"):
    """
    Calculate correlations (Spearman or Pearson) for all unique column pairs in CSV files.

    Args:
        csv_dir (str): Path to the directory containing CSV files.
        output_file (str): Path to save the correlation results.
        method (str): Correlation method to use ("spearman" or "pearson").
    """
    correlation_results = []
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('_with_cgRMSD.csv')]

    for csv_file in csv_files:
        native_name = csv_file.replace('_with_cgRMSD.csv', '')
        csv_path = os.path.join(csv_dir, csv_file)
        df = pd.read_csv(csv_path)

        if df.empty:
            print(f"The file {csv_file} is empty. Skipped.")
            continue

        # Ensure all columns are numeric
        numeric_df = df.select_dtypes(include=[np.number])
        non_numeric_columns = set(df.columns) - set(numeric_df.columns)
        # if non_numeric_columns:
        #     print(f"Non-numeric columns skipped in {csv_file}: {non_numeric_columns}")

        correlations = {'Native': native_name}
        column_pairs = combinations(numeric_df.columns, 2)  # Only numeric columns

        for col1, col2 in column_pairs:
            if numeric_df[col1].isna().all() or numeric_df[col2].isna().all():
                # Skip if either column is entirely NaN
                correlations[f"{col1}/{col2}"] = np.nan
                continue

            # Calculate correlation based on the chosen method
            if method == "spearman":
                corr, _ = spearmanr(numeric_df[col1], numeric_df[col2], nan_policy='omit')
            elif method == "pearson":
                corr, _ = pearsonr(numeric_df[col1], numeric_df[col2])
            else:
                raise ValueError("Invalid method. Choose 'spearman' or 'pearson'.")
            
            correlations[f"{col1}/{col2}"] = corr

        correlation_results.append(correlations)

    results_df = pd.DataFrame(correlation_results)
    results_df.to_csv(output_file, index=False)
    print(f"{method.capitalize()} correlation results saved to: {output_file}")

def create_correlation_matrix(correlation_file, output_file):
    """
    Creates a correlation matrix from the provided correlation file.

    Args:
        correlation_file (str): Path to the input CSV file with correlation results.
        output_file (str): Path to save the correlation matrix.
    """
    df = pd.read_csv(correlation_file)
    columns = [col for col in df.columns if col != 'Native']
    tools = sorted(set([col.split('/')[0] for col in columns] + [col.split('/')[1] for col in columns]))
    correlation_matrix = np.zeros((len(tools), len(tools)))

    for col in columns:
        tool_1, tool_2 = col.split('/')
        i = tools.index(tool_1)
        j = tools.index(tool_2)
        correlations = df[col].dropna()
        mean_correlation = correlations.mean() if not correlations.empty else np.nan
        correlation_matrix[i, j] = mean_correlation
        correlation_matrix[j, i] = mean_correlation

    np.fill_diagonal(correlation_matrix, 1)
    correlation_df = pd.DataFrame(correlation_matrix, columns=tools, index=tools)
    correlation_df.to_csv(output_file)
    print(f"Correlation matrix saved to: {output_file}")