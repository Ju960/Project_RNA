import os
import pandas as pd
from Bio.PDB import PDBParser
import numpy as np
from scipy.spatial.transform import Rotation as R

def compute_rmsd(true_atoms, pred_atoms):
    """
    Computes the aligned RMSD between native and predicted atoms.
    :param true_atoms: np.array of native coordinates
    :param pred_atoms: np.array of predicted coordinates
    :return: RMSD (float)
    """
    if true_atoms.shape != pred_atoms.shape:
        raise ValueError("The sizes of native and predicted sequences do not match.")
    rotation, rmsd = R.align_vectors(true_atoms, pred_atoms)
    return rmsd

def extract_atoms(pdb_file, atom_names):
    """
    Extracts the coordinates of specified atoms from a PDB file.
    :param pdb_file: Path to the PDB file
    :param atom_names: List of atom names to extract
    :return: np.array of coordinates
    """
    coords = []
    with open(pdb_file, 'r') as file:
        for line in file:
            if line.startswith("ATOM"):
                atom_name = line[12:16].strip()
                if atom_name in atom_names:
                    coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

def process_native_predictions(native_path, pred_dir, score_file):
    """
    Computes coarse-grained RMSDs for each atom combination and appends them to the score file.
    :param native_path: Path to the native PDB file
    :param pred_dir: Directory containing PDB predictions
    :param score_file: CSV file with scores
    """
    native_coords = extract_atoms(native_path, {atom for comb in ATOM_COMBINATIONS for atom in comb})
    df_scores = pd.read_csv(score_file)
    
    # Initialize columns for each atom combination
    for combination in ATOM_COMBINATIONS:
        col_name = f"RMSD_{'_'.join(combination)}"
        df_scores[col_name] = np.nan

    for idx, row in df_scores.iterrows():
        pred_file = os.path.join(pred_dir, row["Prediction_File"])  # Ensure the CSV file contains a "Prediction_File" column
        if not os.path.exists(pred_file):
            continue
        for combination in ATOM_COMBINATIONS:
            try:
                pred_coords = extract_atoms(pred_file, combination)
                rmsd = compute_rmsd(native_coords, pred_coords)
                df_scores.at[idx, f"RMSD_{'_'.join(combination)}"] = rmsd
            except ValueError:
                print(f"Alignment error for prediction {pred_file} with combination {combination}.")
    
    df_scores.to_csv(score_file, index=False)