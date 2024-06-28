from collections import defaultdict
import pandas as pd

# Correct file paths
input_file_path = "output_sequences.txt"
output_file_path = "codon_frequencies.csv"

# List of all possible codons in alphabetical order starting from 'AAA'
bases = ['A', 'C', 'G', 'T']
codons = sorted([a + b + c for a in bases for b in bases for c in bases])

# Function to read sequences from the file
def read_sequences(file_path):
    sequences = {}
    with open(file_path, 'r') as f:
        current_label = None
        current_sequence = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_label is not None:
                    sequences[current_label] = ' '.join(current_sequence).replace(' ', '')
                current_label = line[1:].strip()
                current_sequence = []
            else:
                current_sequence.append(line)
        if current_label is not None:
            sequences[current_label] = ' '.join(current_sequence).replace(' ', '')
    return sequences

# Function to count codon frequencies in a sequence
def count_codons(sequence):
    codon_count = defaultdict(int)
    codons_in_sequence = [sequence[i:i+3] for i in range(0, len(sequence), 3)]
    for codon in codons_in_sequence:
        if codon != '---' and len(codon) == 3:
            codon_count[codon] += 1
    return codon_count

# Read sequences
sequences = read_sequences(input_file_path)

# Initialize codon frequency matrix
codon_frequencies = {label: {codon: 0 for codon in codons} for label in sequences.keys()}

# Count codon frequencies for each sequence
for label, sequence in sequences.items():
    codon_count = count_codons(sequence)
    for codon, count in codon_count.items():
        codon_frequencies[label][codon] = count

# Convert to DataFrame for easy export
df = pd.DataFrame.from_dict(codon_frequencies, orient='index', columns=codons)

# Save to CSV
df.to_csv(output_file_path)

print(f"Codon frequency matrix has been written to {output_file_path}")
