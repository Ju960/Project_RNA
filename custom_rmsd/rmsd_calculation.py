import os
import pandas as pd
from Bio.PDB import PDBParser
import numpy as np

def load_structure(file_path, atom_list):
    """
    Load a PDB structure and filter specific atoms.

    Args:
        file_path (str): Path to the PDB file.
        atom_list (list): List of atom combinations for the different cgRMSD calculation.

    Returns:
        np.ndarray: Array of atomic coordinates for the specified atoms.
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
    Compute the RMSD after alignment between native and predicted atoms.

    Args:
        native_atoms (np.ndarray): Coordinates of native atoms.
        pred_atoms (np.ndarray): Coordinates of predicted atoms.

    Returns:
        float: The computed RMSD value.

    Raises:
        ValueError: If the number of atoms does not match between native and predicted structures.
    """
    if native_atoms.shape != pred_atoms.shape:
        raise ValueError("Mismatch in atom count or dimensions between native and prediction.")
    
    # Center both sets of atoms
    native_center = native_atoms.mean(axis=0)
    pred_center = pred_atoms.mean(axis=0)
    native_atoms_centered = native_atoms - native_center
    pred_atoms_centered = pred_atoms - pred_center

    # Align using Kabsch algorithm
    H = pred_atoms_centered.T @ native_atoms_centered
    U, S, Vt = np.linalg.svd(H)
    rotation = U @ Vt
    if np.linalg.det(rotation) < 0:
        Vt[-1, :] *= -1
        rotation = U @ Vt

    # Rotate prediction
    aligned_pred = pred_atoms_centered @ rotation.T

    # Compute RMSD
    rmsd_value = np.sqrt(np.mean(np.linalg.norm(aligned_pred - native_atoms_centered, axis=1)**2))
    return rmsd_value

def process_native_predictions(native_path, pred_dir, score_file, atom_list):
    """
    Add coarse-grained RMSD (cgRMSD) to the score CSV file by processing predictions.

    Args:
        native_path (str): Path to the native PDB file.
        pred_dir (str): Directory containing prediction PDB files.
        score_file (str): Path to the score CSV file.
        atom_list (list of list): List of atom combinations for cgRMSD calculations.
    """
    # Load native structure coordinates for each atom combination
    native_atoms = {}
    for comb in atom_list:
        native_atoms[tuple(comb)] = load_structure(native_path, comb)

    # Load the score file
    scores_df = pd.read_csv(score_file)

    # Get the list of prediction files
    pred_files = sorted(os.listdir(pred_dir))

    # Initialize new columns for cgRMSD
    for comb in atom_list:
        col_name = f"cgRMSD_{'_'.join(comb)}"
        scores_df[col_name] = np.nan  # Placeholder

    for pred_file in pred_files:
        pred_path = os.path.join(pred_dir, pred_file)
        normalized_pred_id = f"normalized_{pred_file}"

        # Find the matching row in the CSV
        matching_row = scores_df[scores_df.iloc[:, 0] == normalized_pred_id]
        if matching_row.empty:
            print(f"No match found for file {pred_file}.")
            continue
        row_index = matching_row.index[0]  # Index of the matching row

        # Load prediction structure coordinates for each atom combination
        pred_atoms = {}
        for comb in atom_list:
            pred_atoms[tuple(comb)] = load_structure(pred_path, comb)

        # Compute cgRMSD for each atom combination
        for comb in atom_list:
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
    print(f"Updated file with cgRMSD: {updated_file}")

def process_all_natives(natives_dir, preds_dir, scores_dir, atom_list):
    """
    Iterate through all native structures in the NATIVES folder and process their predictions.

    Args:
        natives_dir (str): Directory containing native PDB files.
        preds_dir (str): Directory containing prediction subdirectories.
        scores_dir (str): Directory containing score CSV files.
        atom_list (list of list): List of atom combinations for cgRMSD calculations.
    """
    native_files = [f for f in os.listdir(natives_dir) if f.endswith('.pdb')]

    for native_file in native_files:
        native_path = os.path.join(natives_dir, native_file)
        pred_dir = os.path.join(preds_dir, native_file.replace('.pdb', ''))
        score_file = os.path.join(scores_dir, native_file.replace('.pdb', '.csv'))

        if not os.path.exists(pred_dir):
            print(f"Missing prediction directory for {native_file}: {pred_dir}")
            continue
        if not os.path.exists(score_file):
            print(f"Missing score file for {native_file}: {score_file}")
            continue

        print(f"Processing native {native_file}...")
        process_native_predictions(native_path, pred_dir, score_file, atom_list)