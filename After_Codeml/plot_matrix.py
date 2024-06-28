import os
import pandas as pd

def find_entropy_files(root_dir):
    entropy_files = {}
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'entropy_differences.xlsx':
                gene_name = os.path.basename(subdir)
                entropy_files[gene_name] = os.path.join(subdir, file)
    return entropy_files

def get_amino_acid_names(file_path):
    df = pd.read_excel(file_path, nrows=0)  # Read only the header
    return df.columns[2:].tolist()  # Skip 'Node1' and 'Node2', take the rest

def process_entropy_files(entropy_files):
    amino_acid_data = {}
    common_nodes = None

    for gene, file_path in entropy_files.items():
        df = pd.read_excel(file_path)
        amino_acids = get_amino_acid_names(file_path)
        
        if common_nodes is None:
            common_nodes = df[['Node1', 'Node2']].copy()

        for aa in amino_acids:
            if aa not in amino_acid_data:
                amino_acid_data[aa] = []
            temp_df = df[['Node1', 'Node2']].copy()
            temp_df[gene] = df[aa]
            amino_acid_data[aa].append(temp_df)
    
    # Combine dataframes for each amino acid
    for aa in amino_acid_data:
        amino_acid_data[aa] = pd.concat(amino_acid_data[aa], axis=1)
        # Remove duplicate Node1 and Node2 columns
        amino_acid_data[aa] = amino_acid_data[aa].loc[:, ~amino_acid_data[aa].columns.duplicated()]
    
    return amino_acid_data

def create_output_excel(amino_acid_data, output_path):
    with pd.ExcelWriter(output_path) as writer:
        for aa, df in amino_acid_data.items():
            df.to_excel(writer, sheet_name=aa, index=False)

if __name__ == "__main__":
    root_dir = '/Users/kagarwal/Desktop/9560/input_after'  # Replace with the path to your directory
    output_path = 'combined_entropy_differences.xlsx'

    entropy_files = find_entropy_files(root_dir)
    amino_acid_data = process_entropy_files(entropy_files)
    create_output_excel(amino_acid_data, output_path)
