import pandas as pd
import re

# File paths
entropy_file_path = "gene.xlsx"
relation_file_path = "relation.txt"
output_file_path = "entropy_differences.xlsx"

# Read the entropy data
entropy_df = pd.read_excel(entropy_file_path, index_col=0)

# Parse the relation file to get the node connections and tree with labels
with open(relation_file_path, 'r') as file:
    lines = file.readlines()

# Extract the node connections
node_connections = []
tree_with_labels = ""
for line in lines:
    if re.match(r'\s*\d+\.\.\d+', line):
        node_connections.extend(re.findall(r'(\d+)\.\.(\d+)', line))
    if line.startswith("tree with node labels"):
        tree_with_labels = lines[lines.index(line) + 1].strip()

# Extract the node labels and match numbers to labels
node_labels = {}
leaf_nodes = re.findall(r'\d+_[\w_]+', tree_with_labels)
for leaf_node in leaf_nodes:
    number, label = leaf_node.split('_', 1)
    node_labels[int(number)] = label

# Number the internal nodes
num_leaf_nodes = len(node_labels)
internal_node_start = num_leaf_nodes + 1
internal_node_end = num_leaf_nodes + (num_leaf_nodes - 1)
for i in range(internal_node_start, internal_node_end + 1):
    node_labels[i] = f'node #{i}'

# Calculate entropy differences for connected nodes
entropy_differences = []

for node1, node2 in node_connections:
    node1 = node_labels[int(node1)]
    node2 = node_labels[int(node2)]
    
    if node1 in entropy_df.index and node2 in entropy_df.index:
        entropy_diff = entropy_df.loc[node1] - entropy_df.loc[node2]
        entropy_differences.append((node1, node2, entropy_diff))

# Create a DataFrame to store the entropy differences
diff_data = {
    'Node1': [diff[0] for diff in entropy_differences],
    'Node2': [diff[1] for diff in entropy_differences]
}
for amino_acid in entropy_df.columns:
    diff_data[amino_acid] = [diff[2][amino_acid] for diff in entropy_differences]

diff_df = pd.DataFrame(diff_data)

# Save the entropy differences to a new Excel file
diff_df.to_excel(output_file_path, index=False)

print(f"Entropy differences have been written to {output_file_path}")
