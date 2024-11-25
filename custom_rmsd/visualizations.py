import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_correlation_matrix(correlation_file, output_image):
   """
   Loads a CSV file containing correlations and generates an aesthetically pleasing correlation matrix.
   """
   # Load the data from the CSV file
   df = pd.read_csv(correlation_file, index_col=0)

   # Check if the file contains numeric data
   if df.empty:
       print("The file is empty or incorrectly formatted.")
       return

   # Convert all columns to numeric values
   df = df.apply(pd.to_numeric, errors='coerce')

   # Check for missing values after conversion
   if df.isnull().values.any():
       print("The file contains non-numeric or missing values after conversion.")
       return

   # Create a figure and a grid of axes
   plt.figure(figsize=(10, 8))

   # Create the correlation matrix with Seaborn
   sns.set(style='white')  # Choose a white background style
   cmap = sns.diverging_palette(230, 20, as_cmap=True)  # Diverging color palette to better visualize positive and negative values
   ax = sns.heatmap(df, annot=True, cmap=cmap, fmt='.2f', cbar_kws={'shrink': .8}, linewidths=0.5)

   # Add titles and labels
   plt.title('Correlation Matrix of Scores', fontsize=16)
   plt.xlabel('Metrics', fontsize=14)
   plt.ylabel('Metrics', fontsize=14)

   # Save the image
   plt.tight_layout()
   plt.savefig(output_image)
   plt.show()