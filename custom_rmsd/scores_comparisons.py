import pandas as pd
import os

def concat_files(input_folder, output_file):
    """
    Concatenates all CSV files in the specified folder that match a certain naming pattern 
    (e.g., files containing "with_cgRMSD" in their name) and adds a 'native' column containing 
    the native name extracted from the filename. Saves the result to a single CSV file.
    """
    # List to store DataFrames
    all_data = []
    
    # Iterate over all files in the input folder
    for file_name in os.listdir(input_folder):
        # Check if the file is a CSV and matches the expected naming pattern
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
    
    # Concatenate all DataFrames into a single one
    concatenated_df = pd.concat(all_data, ignore_index=True)
    
    # Save the concatenated DataFrame to the output CSV file
    concatenated_df.to_csv(output_file, index=False)
    print(f"Concatenated file saved to {output_file}")