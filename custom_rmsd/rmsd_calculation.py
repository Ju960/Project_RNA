import os
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from scipy.spatial.transform import Rotation as R

def load_structure(file_path, atom_list):
    """
    Loads a PDB structure and filters specified atoms.
    :param file_path: Path to the PDB file
    :param atom_list: List of atom names to extract
    :return: np.array of atom coordinates
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('model', file_path)
    atoms = []
    for atom in structure.get_atoms():
        if atom.get_name() in atom_list:
            atoms.append(atom.get_coord())
    return np.array(atoms)

def compute_rmsd(native_atoms, pred_atoms):
    """
    Computes RMSD after superposition.
    :param native_atoms: np.array of native atom coordinates
    :param pred_atoms: np.array of predicted atom coordinates
    :return: RMSD (float)
    """
    if len(native_atoms) != len(pred_atoms):
        raise ValueError("The number of atoms does not match between native and prediction.")
    rotation, _ = R.align_vectors(pred_atoms, native_atoms)
    aligned_pred = rotation.apply(pred_atoms)
    return np.sqrt(np.mean(np.sum((aligned_pred - native_atoms) ** 2, axis=1)))

def process_native_predictions(native_path, pred_dir, score_file):
    """
    Adds coarse-grained RMSD (cgRMSD) values to the CSV score file by processing predictions.
    :param native_path: Path to the native PDB file
    :param pred_dir: Directory containing prediction PDB files
    :param score_file: Path to the CSV score file
    """
    # Load coordinates for the native structure
    native_atoms = {}
    for comb in ATOM_COMBINATIONS:
        native_atoms[tuple(comb)] = load_structure(native_path, comb)
    
    # Load the CSV file
    scores_df = pd.read_csv(score_file)

    # Retrieve prediction files
    pred_files = sorted(os.listdir(pred_dir))

    # Initialize new columns for each atom combination
    for comb in ATOM_COMBINATIONS:
        col_name = f"cgRMSD_{'_'.join(comb)}"
        scores_df[col_name] = np.nan  # Placeholder for the scores

    # Map prediction files by their names
    pred_file_dict = {os.path.splitext(f)[0]: f for f in pred_files}

    for i, row in scores_df.iterrows():
        # Use the first column (prediction name) to locate the corresponding file
        pred_file_name = row['Prediction_File'].split('.')[0]  # Assumes 'Prediction_File' contains file names, e.g., rp03_1
        if pred_file_name in pred_file_dict:
            pred_path = os.path.join(pred_dir, pred_file_dict[pred_file_name])

            # Load prediction atom coordinates
            pred_atoms = {}
            for comb in ATOM_COMBINATIONS:
                pred_atoms[tuple(comb)] = load_structure(pred_path, comb)
            
            # Compute custom RMSD for each combination
            for comb in ATOM_COMBINATIONS:
                try:
                    rmsd_score = compute_rmsd(native_atoms[tuple(comb)], pred_atoms[tuple(comb)])
                    scores_df.loc[i, f"cgRMSD_{'_'.join(comb)}"] = rmsd_score
                except ValueError as e:
                    print(f"Error for {pred_file_name} with {comb}: {e}")
    
    # Save the updated CSV file
    updated_file = score_file.replace(".csv", "_with_cgRMSD.csv")
    scores_df.to_csv(updated_file, index=False)
    print(f"Updated file with custom RMSD saved: {updated_file}")