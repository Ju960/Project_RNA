import os
import pandas as pd
from Bio.PDB import PDBParser
import numpy as np
from scipy.spatial.transform import Rotation as R

def load_structure(file_path, atom_list):
    """Load a PDB structure and filter the specified atoms."""
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('model', file_path)
    atoms = []
    for atom in structure.get_atoms():
        if atom.get_name() in atom_list:
            atoms.append(atom.get_coord())
    return np.array(atoms)

def compute_rmsd(native_atoms, pred_atoms):
    """Compute the RMSD after superposition."""
    if len(native_atoms) != len(pred_atoms):
        raise ValueError("The number of atoms does not match between the native and predicted structures.")
    rotation, _ = R.align_vectors(pred_atoms, native_atoms)
    aligned_pred = rotation.apply(pred_atoms)
    return np.sqrt(np.mean(np.linalg.norm(aligned_pred - native_atoms, axis=1)))

def process_native_predictions(native_path, pred_dir, score_file):
    """Add cgRMSD to the CSV file by processing the predictions."""
    # Load the native structure atom coordinates
    native_atoms = {}
    for comb in ATOM_COMBINATIONS:
        native_atoms[tuple(comb)] = load_structure(native_path, comb)
    
    # Load the CSV file
    scores_df = pd.read_csv(score_file)

    # List the prediction files
    pred_files = sorted(os.listdir(pred_dir))
    
    # Initialize new columns
    for comb in ATOM_COMBINATIONS:
        col_name = f"cgRMSD_{'_'.join(comb)}"
        scores_df[col_name] = np.nan  # Placeholder

    for pred_file in pred_files:
        pred_path = os.path.join(pred_dir, pred_file)
        
        # Build the filename in the CSV (with 'normalized_' prefix added before the .pdb extension)
        normalized_pred_id = f"normalized_{pred_file}"
        
        # Find the matching row in the CSV
        matching_row = scores_df[scores_df.iloc[:, 0] == normalized_pred_id]
        if matching_row.empty:
            print(f"No match found for file {pred_file}.")
            continue
        row_index = matching_row.index[0]  # Index of the matching row

        # Load the prediction atom coordinates
        pred_atoms = {}
        for comb in ATOM_COMBINATIONS:
            pred_atoms[tuple(comb)] = load_structure(pred_path, comb)
        
        # Calculate custom RMSD for each combination
        for comb in ATOM_COMBINATIONS:
            try:
                rmsd_score = compute_rmsd(native_atoms[tuple(comb)], pred_atoms[tuple(comb)])
                scores_df.loc[row_index, f"cgRMSD_{'_'.join(comb)}"] = rmsd_score
            except ValueError as e:
                print(f"Error for {pred_file} with {comb}: {e}")

    # Drop rows with missing values
    scores_df = scores_df.dropna()

    # Save the updated CSV file
    updated_file = score_file.replace(".csv", "_with_cgRMSD.csv")
    scores_df.to_csv(updated_file, index=False)
    print(f"File updated with custom RMSD (rows with missing values removed): {updated_file}")

def process_all_natives(natives_dir, preds_dir, scores_dir):
    """Process all native files in the NATIVES directory and their corresponding predictions."""
    native_files = [f for f in os.listdir(natives_dir) if f.endswith('.pdb')]

    for native_file in native_files:
        native_path = os.path.join(natives_dir, native_file)
        pred_dir = os.path.join(preds_dir, native_file.replace('.pdb', ''))
        score_file = os.path.join(scores_dir, native_file.replace('.pdb', '.csv'))

        if not os.path.exists(pred_dir):
            print(f"Prediction directory missing for {native_file}: {pred_dir}")
            continue
        if not os.path.exists(score_file):
            print(f"Score file missing for {native_file}: {score_file}")
            continue

        print(f"Processing native {native_file}...")
        process_native_predictions(native_path, pred_dir, score_file)
