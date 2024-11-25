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
    """Compute the RMSD after alignment."""
    if len(native_atoms) != len(pred_atoms):
        raise ValueError("The number of atoms does not match between the native and predicted structures.")
    rotation, _ = R.align_vectors(pred_atoms, native_atoms)
    aligned_pred = rotation.apply(pred_atoms)
    return np.sqrt(np.mean(np.linalg.norm(aligned_pred - native_atoms, axis=1)))

def process_native_predictions(native_path, pred_dir, score_file):
    """Add cgRMSD to the CSV file by processing predictions."""
    # Load the coordinates of the native structure
    native_atoms = {}
    for comb in ATOM_COMBINATIONS:
        native_atoms[tuple(comb)] = load_structure(native_path, comb)
    
    # Load the CSV file
    scores_df = pd.read_csv(score_file)

    # Loop through the prediction files in the directory
    pred_files = sorted(os.listdir(pred_dir))
    if len(pred_files) != len(scores_df):
        raise ValueError("The number of predictions does not match the number of rows in the CSV file.")
    
    # Initialize the new columns
    for comb in ATOM_COMBINATIONS:
        col_name = f"cgRMSD_{'_'.join(comb)}"
        scores_df[col_name] = np.nan  # Placeholder

    for i, pred_file in enumerate(pred_files):
        pred_path = os.path.join(pred_dir, pred_file)
        
        # Construct the file name in the CSV (with 'normalized_' added before the .pdb extension)
        normalized_pred_id = f"normalized_{pred_file}"
        
        # Find the matching row in the CSV
        matching_row = scores_df[scores_df.iloc[:, 0] == normalized_pred_id]
        if matching_row.empty:
            print(f"No match found for file {pred_file}.")
            continue
        row_index = matching_row.index[0]  # Index of the matching row

        # Load the atoms from the prediction
        pred_atoms = {}
        for comb in ATOM_COMBINATIONS:
            pred_atoms[tuple(comb)] = load_structure(pred_path, comb)
        
        # Compute the custom RMSD for each atom combination
        for comb in ATOM_COMBINATIONS:
            try:
                rmsd_score = compute_rmsd(native_atoms[tuple(comb)], pred_atoms[tuple(comb)])
                scores_df.loc[row_index, f"cgRMSD_{'_'.join(comb)}"] = rmsd_score
            except ValueError as e:
                print(f"Error for {pred_file} with {comb}: {e}")

    # Save the updated CSV file
    updated_file = score_file.replace(".csv", "_with_cgRMSD.csv")
    scores_df.to_csv(updated_file, index=False)
    print(f"File updated with custom RMSD: {updated_file}")