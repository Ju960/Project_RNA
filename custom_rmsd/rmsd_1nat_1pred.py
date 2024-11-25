import os
import pandas as pd
import numpy as np
from  rmsd_calculation import load_structure, compute_rmsd

# Fonction de traitement des prédictions
def process_native_predictions(native_path, pred_path, score_file, atom_list):
    """
    Add coarse-grained RMSD (cgRMSD) to the score CSV file by processing predictions.

    Args:
        native_path (str): Path to the native PDB file.
        pred_path (str): Path to the prediction PDB file.
        score_file (str): Path to the score CSV file.
        atom_list (list of list): List of atom combinations for cgRMSD calculations.
    """

    # Charger les coordonnées des atomes de la structure native pour chaque combinaison d'atomes
    native_atoms = {}
    for comb in atom_list:
        native_atoms[tuple(comb)] = load_structure(native_path, comb)

    # Charger le fichier CSV des scores
    scores_df = pd.read_csv(score_file)

    # Initialiser de nouvelles colonnes pour le cgRMSD
    for comb in atom_list:
        col_name = f"cgRMSD_{'_'.join(comb)}"
        scores_df[col_name] = np.nan  # Placeholders pour les scores

    # Extraire l'ID de la prédiction à partir du nom du fichier de prédiction
    pred_file_name = os.path.basename(pred_path)
    normalized_pred_id = f"normalized_{pred_file_name}"

    # Trouver la ligne correspondante dans le CSV
    matching_row = scores_df[scores_df.iloc[:, 0] == normalized_pred_id]
    if matching_row.empty:
        print(f"No match found for file {pred_file_name}.")
    else:
        row_index = matching_row.index[0]  # Index de la ligne correspondante

        # Charger les coordonnées de la prédiction pour chaque combinaison d'atomes
        pred_atoms = {}
        for comb in atom_list:
            pred_atoms[tuple(comb)] = load_structure(pred_path, comb)

        # Calculer le cgRMSD pour chaque combinaison d'atomes
        for comb in atom_list:
            try:
                rmsd_score = compute_rmsd(native_atoms[tuple(comb)], pred_atoms[tuple(comb)])
                scores_df.loc[row_index, f"cgRMSD_{'_'.join(comb)}"] = rmsd_score
            except ValueError as e:
                print(f"Error for {pred_file_name} with {comb}: {e}")

    # Supprimer les lignes avec des valeurs manquantes
    scores_df = scores_df.dropna()

    # Sauvegarder le fichier CSV mis à jour
    updated_file = score_file.replace(".csv", "_1pred.csv")
    scores_df.to_csv(updated_file, index=False)
    print(f"Updated file with cgRMSD: {updated_file}")

# Fonction main
def main():
    # Définir le chemin du fichier native et du fichier de prédiction
    native_path = '/Users/oceanesaibou/Desktop/GENIOMHE/S3/Bioinformatics_RNA/Project_2/TEST_PACKAGE/NATIVE/rp03.pdb'  # Remplacez par le chemin réel de votre fichier native
    pred_path = '/Users/oceanesaibou/Desktop/GENIOMHE/S3/Bioinformatics_RNA/Project_2/TEST_PACKAGE/PREDS/rp03/3drna_rp03_1.pdb'  # Remplacez par le chemin réel de votre fichier prédiction

    # Chemin vers le fichier CSV des scores
    score_file = '/Users/oceanesaibou/Desktop/GENIOMHE/S3/Bioinformatics_RNA/Project_2/TEST_PACKAGE/SCORES/rp03.csv'  # Remplacez par le chemin réel de votre fichier CSV

    # Liste des combinaisons d'atomes pour le calcul du cgRMSD
    atom_list = [
        ["C1'","C2'"],  # Exemple de combinaison d'atomes (carbone, azote, oxygène)
        ["P", "O1'"]  # Autre exemple de combinaison d'atomes (carbone alpha, azote, etc.)
    ]

    # Appeler la fonction pour traiter les prédictions et ajouter les scores cgRMSD au fichier CSV
    process_native_predictions(native_path, pred_path, score_file, atom_list)

# Appel de la fonction main
if __name__ == "__main__":
    main()