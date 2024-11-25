import os
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import pearsonr


def calculate_spearman_correlations(csv_dir, output_file):
    """
    Calculates the Spearman correlations for each native, including between baseline scores,
    and saves the results in a CSV file.
    """
    correlation_results = []


    # Iterate over the generated CSV files
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('_with_cgRMSD.csv')]


    for csv_file in csv_files:
        native_name = csv_file.replace('_with_cgRMSD.csv', '')
        csv_path = os.path.join(csv_dir, csv_file)
        
        # Load the CSV file
        df = pd.read_csv(csv_path)
        
        # Check if it is not empty
        if df.empty:
            print(f"The file {csv_file} is empty. Skipping.")
            continue


        # Initialize a dictionary to store the correlations for this native
        correlations = {'Native': native_name}
        
        # Get the baseline columns and cgRMSD columns
        base_metrics = ['RMSD', 'MCQ', 'TM-score']
        cgRMSD_columns = [col for col in df.columns if col.startswith('cgRMSD_')]
        
        # Calculate the correlations between the baseline scores
        for i, base_metric_1 in enumerate(base_metrics):
            for base_metric_2 in base_metrics[i+1:]:
                spearman_corr, _ = spearmanr(df[base_metric_1], df[base_metric_2])
                correlations[f"{base_metric_1}/{base_metric_2}"] = spearman_corr


        # Calculate the correlations between each baseline score and each cgRMSD
        for base_metric in base_metrics:
            for cgRMSD_col in cgRMSD_columns:
                spearman_corr, _ = spearmanr(df[base_metric], df[cgRMSD_col])
                correlations[f"{base_metric}/{cgRMSD_col}"] = spearman_corr
        
        # Add the results for this native to the list
        correlation_results.append(correlations)


    # Convert the results into a DataFrame
    results_df = pd.DataFrame(correlation_results)
    
    # Save to a CSV file
    results_df.to_csv(output_file, index=False)
    print(f"Correlation CSV file saved at: {output_file}")


def calculate_pearson_correlations(csv_dir, output_file):
    """
    Calculates the Pearson correlations for each native, including between baseline scores,
    and saves the results in a CSV file.
    """
    correlation_results = []


    # Iterate over the generated CSV files
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('_with_cgRMSD.csv')]


    for csv_file in csv_files:
        native_name = csv_file.replace('_with_cgRMSD.csv', '')
        csv_path = os.path.join(csv_dir, csv_file)
        
        # Load the CSV file
        df = pd.read_csv(csv_path)
        
        # Check if it is not empty
        if df.empty:
            print(f"The file {csv_file} is empty. Skipping.")
            continue


        # Initialize a dictionary to store the correlations for this native
        correlations = {'Native': native_name}
        
        # Get the baseline columns and cgRMSD columns
        base_metrics = ['RMSD', 'MCQ', 'TM-score']
        cgRMSD_columns = [col for col in df.columns if col.startswith('cgRMSD_')]
        
        # Calculate the correlations between the baseline scores
        for i, base_metric_1 in enumerate(base_metrics):
            for base_metric_2 in base_metrics[i+1:]:
                pearson_corr, _ = pearsonr(df[base_metric_1], df[base_metric_2])
                correlations[f"{base_metric_1}/{base_metric_2}"] = pearson_corr


        # Calculate the correlations between each baseline score and each cgRMSD
        for base_metric in base_metrics:
            for cgRMSD_col in cgRMSD_columns:
                pearson_corr, _ = pearsonr(df[base_metric], df[cgRMSD_col])
                correlations[f"{base_metric}/{cgRMSD_col}"] = pearson_corr
        
        # Add the results for this native to the list
        correlation_results.append(correlations)


    # Convert the results into a DataFrame
    results_df = pd.DataFrame(correlation_results)
    
    # Save to a CSV file
    results_df.to_csv(output_file, index=False)
    print(f"Correlation CSV file saved at: {output_file}")



def create_correlation_matrix(correlation_file, output_file):
   """Crée une matrice de corrélation à partir du fichier des corrélations de Spearman."""
  
   # Charger les données du fichier de corrélations
   df = pd.read_csv(correlation_file)
  
   # Extraire les noms des outils à partir des colonnes
   columns = [col for col in df.columns if col != 'Native']
  
   # Extraire les outils uniques à partir des noms des colonnes (avant le slash)
   tools = sorted(set([col.split('/')[0] for col in columns] + [col.split('/')[1] for col in columns]))
  
   # Créer une matrice vide pour les corrélations
   correlation_matrix = np.zeros((len(tools), len(tools)))
  
   # Remplir la matrice avec les moyennes des corrélations
   for col in columns:
       tool_1, tool_2 = col.split('/')
      
       # Trouver les indices des outils dans la liste 'tools'
       i = tools.index(tool_1)
       j = tools.index(tool_2)
      
       # Extraire la corrélation de la colonne
       correlations = df[col].dropna()
       mean_correlation = correlations.mean() if not correlations.empty else np.nan
      
       # Placer la corrélation dans la matrice (symétriquement)
       correlation_matrix[i, j] = mean_correlation
       correlation_matrix[j, i] = mean_correlation
  
   # Remplir la diagonale avec 1 (corrélation d'un outil avec lui-même)
   np.fill_diagonal(correlation_matrix, 1)
  
   # Convertir la matrice en DataFrame pour une meilleure lisibilité
   correlation_df = pd.DataFrame(correlation_matrix, columns=tools, index=tools)
  
   # Sauvegarder la matrice dans un fichier CSV
   correlation_df.to_csv(output_file)
   print(f"Matrice de corrélation sauvegardée sous : {output_file}")

def create_correlation_matrix(correlation_file, output_file):
   """Creates a correlation matrix from the Spearman correlation file."""
  
   # Load data from the correlation file
   df = pd.read_csv(correlation_file)
  
   # Extract tool names from the columns
   columns = [col for col in df.columns if col != 'Native']
  
   # Extract unique tools from the column names (before the slash)
   tools = sorted(set([col.split('/')[0] for col in columns] + [col.split('/')[1] for col in columns]))
  
   # Create an empty matrix for correlations
   correlation_matrix = np.zeros((len(tools), len(tools)))
  
   # Fill the matrix with mean correlations
   for col in columns:
       tool_1, tool_2 = col.split('/')
      
       # Find the indices of the tools in the 'tools' list
       i = tools.index(tool_1)
       j = tools.index(tool_2)
      
       # Extract the correlation from the column
       correlations = df[col].dropna()
       mean_correlation = correlations.mean() if not correlations.empty else np.nan
      
       # Place the correlation in the matrix (symmetrically)
       correlation_matrix[i, j] = mean_correlation
       correlation_matrix[j, i] = mean_correlation
  
   # Fill the diagonal with 1 (correlation of a tool with itself)
   np.fill_diagonal(correlation_matrix, 1)
  
   # Convert the matrix to a DataFrame for better readability
   correlation_df = pd.DataFrame(correlation_matrix, columns=tools, index=tools)
  
   # Save the matrix to a CSV file
   correlation_df.to_csv(output_file)
   print(f"Correlation matrix saved as: {output_file}")

