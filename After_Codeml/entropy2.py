import pandas as pd
import numpy as np

# File paths
input_file_path = "amino_acid_codon_probabilities.xlsx"
output_file_path = "gene.xlsx"

# Threshold for numerical precision
threshold = 1e-9

# Function to calculate Shannon entropy with a dynamic base
def calculate_entropy(probabilities, base):
    # Calculate the entropy using the specified base for the logarithm
    entropy = -np.sum(probabilities * np.log(probabilities + threshold) / np.log(base))
    # Ensure entropy is not negative due to precision errors
    return max(entropy, 0) if entropy < threshold else entropy

# Amino acids to exclude
excluded_amino_acids = ['Methionine', 'Tryptophan']

# Dictionary to store entropy values for each amino acid
entropy_data = {}

# Read the input Excel file
with pd.ExcelFile(input_file_path) as xls:
    # Iterate over each sheet (each amino acid)
    for sheet_name in xls.sheet_names:
        # Skip excluded amino acids
        if sheet_name in excluded_amino_acids:
            continue
        # Read the data from the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name=sheet_name, index_col=0)
        # Calculate the base for the logarithm: the number of codons (columns) for this amino acid
        base = df.shape[1]
        # Calculate entropy for each row (node label) using the number of codons as the base
        entropies = df.apply(lambda row: calculate_entropy(row, base), axis=1)
        # Store the entropies in the dictionary with amino acid as key
        entropy_data[sheet_name] = entropies

# Convert the dictionary to a DataFrame
entropy_df = pd.DataFrame(entropy_data)

# Write the DataFrame to an Excel file
entropy_df.to_excel(output_file_path, sheet_name='Entropy Matrix')

print(f"Amino acid codon entropy matrix has been written to {output_file_path}")
