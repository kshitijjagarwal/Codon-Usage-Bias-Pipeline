import pandas as pd

# File paths
input_file_path = "amino_acid_codon_frequencies.xlsx"
output_file_path = "amino_acid_codon_probabilities.xlsx"

# Read the input Excel file
with pd.ExcelWriter(output_file_path) as writer:
    with pd.ExcelFile(input_file_path) as xls:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name, index_col=0)
            # Calculate probabilities
            probabilities = df.div(df.sum(axis=1), axis=0)
            # Write to a new sheet in the output Excel file
            probabilities.to_excel(writer, sheet_name=sheet_name)

print(f"Amino acid codon probability matrices have been written to {output_file_path}")
