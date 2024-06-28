import os
import re
import pandas as pd

def extract_species_from_newick(newick_content):
    """Extracts species names from a Newick formatted string using regular expressions."""
    species_pattern = re.compile(r'(\b[A-Za-z]+(?:_[A-Za-z]+)+\b)')
    return re.findall(species_pattern, newick_content)

def parse_tree_files_to_matrix(directory_path):
    """Creates a matrix from tree files mapping species presence across files and saves it as an Excel file."""
    species_to_files = {}
    all_species = set()
    files = [f for f in os.listdir(directory_path) if f.endswith(".rootree")]

    # First, collect all species and map them to files
    for filename in files:
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        species_list = extract_species_from_newick(content)
        all_species.update(species_list)  # Add new species to the set
        for species in species_list:
            if species not in species_to_files:
                species_to_files[species] = []
            species_to_files[species].append(filename)

    # Create a DataFrame with all species as rows and files as columns
    # Initialize with 'N' (no presence)
    matrix = pd.DataFrame('N', index=sorted(all_species), columns=files)

    # Fill the matrix with 'Y' where species is present
    for species, file_list in species_to_files.items():
        matrix.loc[species, file_list] = 'Y'

    # Save the matrix to an Excel file in the same directory
    excel_path = os.path.join(directory_path, 'species_presence_matrix.xlsx')
    matrix.to_excel(excel_path, index=True)

    return matrix, excel_path

# Usage
directory_path = '/Users/kshitij_mac/Desktop/9560/simplified_trees'  # Replace with the path to your directory containing tree files
presence_matrix, output_path = parse_tree_files_to_matrix(directory_path)
print("Matrix saved to:", output_path)
