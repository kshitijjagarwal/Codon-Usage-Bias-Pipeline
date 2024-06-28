import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile
import shutil

# Set a default font to avoid the macOS font warning
plt.rcParams['font.family'] = 'DejaVu Sans'

# Load the combined entropy differences file
combined_file_path = 'combined_entropy_differences.xlsx'  # Replace with the actual path to your file
combined_df = pd.read_excel(combined_file_path, sheet_name=None)

# Create output directory for histograms
output_dir = 'histograms'
os.makedirs(output_dir, exist_ok=True)

# Plot histograms for each amino acid and each branch
for aa, df in combined_df.items():
    for index, row in df.iterrows():
        branch_name = f"{row['Node1']}_to_{row['Node2']}".replace("/", "_").replace(" ", "_")
        entropy_values = row[2:].dropna()
        
        plt.figure(figsize=(10, 6))
        plt.hist(entropy_values, bins=30, edgecolor='black')
        plt.title(f'Entropy Differences for {aa} - Branch: {branch_name}')
        plt.xlabel('Entropy Difference')
        plt.ylabel('Frequency')
        
        # Save the plot
        plot_path = os.path.join(output_dir, f'{aa}_{branch_name}.png')
        plt.savefig(plot_path)
        plt.close()

# Create a zip file of the histograms
shutil.make_archive(output_dir, 'zip', output_dir)

print(f'Histograms saved and zipped in: {output_dir}.zip')
