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

def plot_metrics_vs_cgRMSD(input_file, output_folder):
    """
    Creates plots for each pair of base metric vs cgRMSD,
    coloring the points by the native, and saves the plots in a given folder.
    """
    # Load the concatenated CSV file
    df = pd.read_csv(input_file)

    # List of columns corresponding to base metrics
    base_metrics = ['RMSD', 'MCQ', 'TM-score']
  
    # List of columns corresponding to cgRMSD scores
    cgRMSD_metrics = ['cgRMSD_P_C1\'_C3\'', 'cgRMSD_P_C1\'_C2\'', 'cgRMSD_O1\'_O3\'_O5\'',
                      'cgRMSD_P_C4\'_C5\'', 'cgRMSD_C4\'_C5\'_O1\'']

    # Get the unique list of natives
    natives = df['native'].unique()

    # Create a distinct color palette using tab20
    palette = sns.color_palette("tab20", len(natives))  # tab20 contains 20 distinct colors
    native_color_map = {native: palette[i] for i, native in enumerate(natives)}  # Mapping natives to colors

    # Create a plot for each combination of base_metric vs cgRMSD_metric
    for base_metric in base_metrics:
        for cgRMSD_metric in cgRMSD_metrics:
            # Create the plot
            plt.figure(figsize=(8, 6))
          
            # Use the scatterplot function with the custom color palette
            sns.scatterplot(x=df[cgRMSD_metric], y=df[base_metric], hue=df['native'],
                            palette=native_color_map, s=100, edgecolor='black', legend='full')
          
            # Add titles and labels
            plt.title(f'{cgRMSD_metric} vs {base_metric}', fontsize=16)
            plt.xlabel(cgRMSD_metric, fontsize=14)
            plt.ylabel(base_metric, fontsize=14)
          
            # Add a legend
            plt.legend(title='Native', bbox_to_anchor=(1.05, 1), loc='upper left')
          
            # Save the plot
            plot_filename = f'{cgRMSD_metric}_vs_{base_metric}.png'
            plot_filepath = f'{output_folder}/{plot_filename}'
            plt.tight_layout()
            plt.savefig(plot_filepath)
            plt.close()  # Close the figure to avoid overloading memory
  
    print(f"All plots have been saved in {output_folder}")