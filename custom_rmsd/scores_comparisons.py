import pandas as pd
import os


def concat_files(input_folder, output_file):
   """
   Concatenate all CSV files in the given folder that match a certain name format (e.g., rp03_with_cgRMSD.csv)
   and add a 'native' column with the native name extracted from the file.
   Save the result in a CSV file.
   """
   # List to store DataFrames
   all_data = []
  
   # Iterate over all files in the input folder
   for file_name in os.listdir(input_folder):
       # Check if the file is a CSV file and matches the expected format
       if file_name.endswith(".csv") and "with_cgRMSD" in file_name:
           file_path = os.path.join(input_folder, file_name)
          
           # Load the CSV file
           df = pd.read_csv(file_path)
          
           # Extract the native name before '_with_cgRMSD'
           native_name = file_name.split('_')[0]
          
           # Add a 'native' column with the extracted native name
           df['native'] = native_name
          
           # Add the DataFrame to the list
           all_data.append(df)
  
   # Concatenate all DataFrames into one
   concatenated_df = pd.concat(all_data, ignore_index=True)
  
   # Save the concatenated DataFrame into a CSV file
   concatenated_df.to_csv(output_file, index=False)
   print(f"Concatenated file saved as {output_file}")