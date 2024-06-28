import os
import pandas as pd
from Bio import SeqIO

def get_common_files(directory_path, excel_file_name, species_list):
    """
    Retrieves common files from the matrix where all specified species are present.
    
    Args:
    directory_path (str): Path to the directory containing the Excel file.
    excel_file_name (str): Name of the Excel file containing the species presence matrix. for us- species_presence_matrix.xlsx'

    species_list (list): List of cleaned species names.

    Returns:
    list: List of filenames where all specified species are present.
    """
    # Load the Excel file
    excel_path = os.path.join(directory_path, excel_file_name)
    matrix = pd.read_excel(excel_path, index_col=0)
    
    # Debugging: Check if all species are in the matrix
    missing_species = [sp for sp in species_list if sp not in matrix.index]
    if missing_species:
        print(f"Error: The following species are not found in the matrix: {', '.join(missing_species)}")
        return []

    # Filter the matrix to include only the rows for the specified species
    filtered_matrix = matrix.loc[species_list]
    
    # Find all files where these species are marked 'Y'
    common_files = filtered_matrix.columns[(filtered_matrix == 'Y').all()].tolist()
    return common_files

def extract_and_save_sequences(ortho_directory, common_files, species_list, output_directory):
    """
    Extracts sequences for specified species from common .fasta files and saves them in separate directories.
    Each output file is named 'msa.fasta' within its specific directory.
    
    Args:
    ortho_directory (str): Directory containing .fasta files.
    common_files (list): List of common filenames to look for in .fasta format.
    species_list (list): Species for which sequences are extracted.
    output_directory (str): Directory to save new sequence files.
    """
    for tree_file in common_files:
        # Apply the file naming transformation rule
        fasta_filename = tree_file.replace('simplified_', '').replace('.rootree', '') + '.fasta'
        fasta_path = os.path.join(ortho_directory, fasta_filename)
        
        if os.path.exists(fasta_path):
            record_dict = SeqIO.to_dict(SeqIO.parse(fasta_path, "fasta"))
            missing_from_fasta = [sp for sp in species_list if sp not in record_dict]
            if missing_from_fasta:
                print(f"Warning: The following species are not found in {fasta_filename}: {', '.join(missing_from_fasta)}")
                continue

            selected_records = [record_dict[sp] for sp in species_list if sp in record_dict]

            # Create a directory for each file and save the sequences there
            individual_output_dir = os.path.join(output_directory, tree_file.replace('simplified_', '').replace('.rootree', ''))
            if not os.path.exists(individual_output_dir):
                os.makedirs(individual_output_dir)
            
            output_path = os.path.join(individual_output_dir, 'msa.fasta')  # Standard file name for all directories
            SeqIO.write(selected_records, output_path, "fasta")
        else:
            print(f"Warning: .fasta file {fasta_filename} not found in {ortho_directory}.")

# Main execution block
if __name__ == "__main__":
    directory_path = '/Users/kshitij_mac/Desktop/9560/simplified_trees/'
    ortho_directory = '/Users/kshitij_mac/Desktop/9560/omm_filtered_NT_CDS 2'
    output_directory = '/Users/kshitij_mac/Desktop/9560/input_paml'
    excel_file_name = 'species_presence_matrix.xlsx'

    print("Enter species names separated by spaces:")
    species_input = input()
    species_list = species_input.strip().split()
    species_list = [sp.strip() for sp in species_list]

    common_files = get_common_files(directory_path, excel_file_name, species_list)
    if common_files:
        extract_and_save_sequences(ortho_directory, common_files, species_list, output_directory)
        print("Sequences extracted and saved.")
    else:
        print("No common files found or missing species errors encountered.")
