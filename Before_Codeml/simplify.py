from Bio import Phylo
from io import StringIO
import os

def simplify_tree(newick_tree):
    # Parse the tree
    tree = Phylo.read(StringIO(newick_tree), "newick")
    
    # Function to remove branch lengths and bootstrap values recursively
    def remove_branch_info(clade):
        clade.branch_length = None
        if hasattr(clade, 'confidence'):
            clade.confidence = None
        for subclade in clade.clades:
            remove_branch_info(subclade)

    # Remove branch lengths and bootstrap values from the root clade
    remove_branch_info(tree.root)

    # Convert tree back to Newick format without branch lengths and bootstrap values
    def format_clade(clade):
        if clade.clades:
            return '({}){}'.format(','.join(format_clade(c) for c in clade.clades), clade.name if clade.name else '')
        else:
            return clade.name if clade.name else ''

    # Start the conversion from the root clade
    simplified_tree = '({});'.format(','.join(format_clade(c) for c in tree.root.clades))

    return simplified_tree

def process_trees(input_folder):
    # List all tree files in the given input folder with .rootree extension
    tree_files = [f for f in os.listdir(input_folder) if f.endswith('.rootree')]
    
    for file_name in tree_files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(input_folder, f'simplified_{file_name}')
        
        # Read tree input from the file
        with open(input_file_path, 'r') as file:
            newick_tree = file.read().strip()
        
        # Simplify the tree
        simplified_tree = simplify_tree(newick_tree)
        
        # Write simplified tree to a file
        with open(output_file_path, 'w') as file:
            file.write(simplified_tree)
        
        print(f"Simplified tree written to {output_file_path}")

# Example usage
input_folder = '/Users/kshitij_mac/Desktop/9560/trees'
process_trees(input_folder)
