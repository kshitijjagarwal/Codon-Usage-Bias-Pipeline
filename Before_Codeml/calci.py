import os
import pandas as pd

def calculate_intersection_files(directory_path, excel_file_name, species_list):
    """
    Calculates the intersection of files in which all the specified species are present.
    
    Args:
    directory_path (str): Path to the directory containing the Excel file- species_presence_matrix.xlsx.
    excel_file_name (str): Name of the Excel file containing the species presence matrix. Here (species_presence_matrix.xlsx)
    species_list (list): List of species names to check for file intersection.

    Returns:
    int: Total number of files where all specified species are present.
    """
    # Load the Excel file
    excel_path = os.path.join(directory_path, excel_file_name)
    matrix = pd.read_excel(excel_path, index_col=0)
    
    # Ensure all species in the input list are present in the matrix to avoid KeyError
    missing_species = [sp for sp in species_list if sp not in matrix.index]
    if missing_species:
        print(f"Warning: The following species were not found in the matrix and will be ignored: {', '.join(missing_species)}")
        species_list = [sp for sp in species_list if sp not in missing_species]

    # Filter the matrix to include only the rows for the specified species
    filtered_matrix = matrix.loc[species_list]
    
    # Calculate the intersection (all files where these species are marked 'Y')
    intersection_count = (filtered_matrix == 'Y').all().sum()
    
    return intersection_count

# Usage Example
if __name__ == "__main__":
    directory_path = '/Users/kshitij_mac/Desktop/9731_orthomam/trees'  # Directory path where species presence matrix is present
    excel_file_name = 'species_presence_matrix.xlsx'  # Ensure this is the correct file name
    print("Enter species names separated by spaces:")
    species_input = input()  # User inputs species names separated by spaces
    species_list = species_input.split()  # Split input string into a list of species names

    # Call the function
    intersection_files_count = calculate_intersection_files(directory_path, excel_file_name, species_list)
    print(f"Total number of files where all specified species are present: {intersection_files_count}")
