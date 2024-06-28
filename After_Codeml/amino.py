import pandas as pd

# File paths
input_file_path = "codon_frequencies.csv"
output_file_path = "amino_acid_codon_frequencies.xlsx"

# Standard genetic code
genetic_code = {
    'TTT': 'Phenylalanine', 'TTC': 'Phenylalanine', 'TTA': 'Leucine', 'TTG': 'Leucine',
    'CTT': 'Leucine', 'CTC': 'Leucine', 'CTA': 'Leucine', 'CTG': 'Leucine',
    'ATT': 'Isoleucine', 'ATC': 'Isoleucine', 'ATA': 'Isoleucine', 'ATG': 'Methionine',
    'GTT': 'Valine', 'GTC': 'Valine', 'GTA': 'Valine', 'GTG': 'Valine',
    'TCT': 'Serine', 'TCC': 'Serine', 'TCA': 'Serine', 'TCG': 'Serine',
    'CCT': 'Proline', 'CCC': 'Proline', 'CCA': 'Proline', 'CCG': 'Proline',
    'ACT': 'Threonine', 'ACC': 'Threonine', 'ACA': 'Threonine', 'ACG': 'Threonine',
    'GCT': 'Alanine', 'GCC': 'Alanine', 'GCA': 'Alanine', 'GCG': 'Alanine',
    'TAT': 'Tyrosine', 'TAC': 'Tyrosine', 'TAA': 'Stop', 'TAG': 'Stop',
    'CAT': 'Histidine', 'CAC': 'Histidine', 'CAA': 'Glutamine', 'CAG': 'Glutamine',
    'AAT': 'Asparagine', 'AAC': 'Asparagine', 'AAA': 'Lysine', 'AAG': 'Lysine',
    'GAT': 'Aspartic Acid', 'GAC': 'Aspartic Acid', 'GAA': 'Glutamic Acid', 'GAG': 'Glutamic Acid',
    'TGT': 'Cysteine', 'TGC': 'Cysteine', 'TGA': 'Stop', 'TGG': 'Tryptophan',
    'CGT': 'Arginine', 'CGC': 'Arginine', 'CGA': 'Arginine', 'CGG': 'Arginine',
    'AGT': 'Serine', 'AGC': 'Serine', 'AGA': 'Arginine', 'AGG': 'Arginine',
    'GGT': 'Glycine', 'GGC': 'Glycine', 'GGA': 'Glycine', 'GGG': 'Glycine'
}

# Reverse the genetic code to map amino acids to codons
amino_acid_to_codons = {}
for codon, amino_acid in genetic_code.items():
    if amino_acid not in amino_acid_to_codons:
        amino_acid_to_codons[amino_acid] = []
    amino_acid_to_codons[amino_acid].append(codon)

# Read codon frequency matrix
codon_frequencies = pd.read_csv(input_file_path, index_col=0)

# Create and write matrices for each amino acid
with pd.ExcelWriter(output_file_path) as writer:
    for amino_acid, codons in amino_acid_to_codons.items():
        if amino_acid == 'Stop':  # Skip stop codons
            continue
        # Create a matrix for the amino acid
        amino_acid_matrix = codon_frequencies[codons]
        # Write to an Excel sheet
        amino_acid_matrix.to_excel(writer, sheet_name=amino_acid)

print(f"Amino acid codon frequency matrices have been written to {output_file_path}")
