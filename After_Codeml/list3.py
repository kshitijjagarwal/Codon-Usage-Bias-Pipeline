from Bio import Phylo
from io import StringIO

# File paths
tree_file_path = "tree.nwk" # you must specify the tree path
sequence_file_path = "extracted_content.txt" # path need not be mentioned as it willbe taken from the same direcotry
output_text_path = "output_sequences.txt"

# Read and parse the Newick tree file
with open(tree_file_path, 'r') as tree_file:
    newick_tree = tree_file.read().strip()
tree = Phylo.read(StringIO(newick_tree), "newick")

# Function to list leaf and internal nodes
def list_nodes(tree):
    leaf_nodes = [clade.name for clade in tree.get_terminals()]
    num_leaf_nodes = len(leaf_nodes)
    internal_nodes = [f"node #{i}" for i in range(num_leaf_nodes + 1, num_leaf_nodes + num_leaf_nodes)]
    return leaf_nodes, internal_nodes

# List leaf and internal nodes
leaf_nodes, internal_nodes = list_nodes(tree)

# Read sequence data and parse it to extract sequences
with open(sequence_file_path, 'r') as seq_file:
    sequence_data = seq_file.read()

# Create a dictionary for sequences
sequences = {}
lines = sequence_data.splitlines()

# Extract sequences for leaf nodes
for i, line in enumerate(lines):
    parts = line.split(maxsplit=1)
    if len(parts) == 2:
        label, sequence = parts
        if label in leaf_nodes:
            sequences[label] = sequence.strip()

# Extract sequences for internal nodes
for internal in internal_nodes:
    for i, line in enumerate(lines):
        if line.startswith(internal):
            sequence = line[10:].strip()
            sequences[internal] = sequence
            break

# Write sequences to output text file in FASTA format
with open(output_text_path, 'w') as output_file:
    for label in leaf_nodes + internal_nodes:
        if label in sequences:
            output_file.write(f">{label}\n{sequences[label]}\n")

print(f"Text file has been written to {output_text_path}")
