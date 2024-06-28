import os
import subprocess

# Path to the main directory containing subdirectories and Python scripts
main_directory = '/Users/kagarwal/Desktop/9560/input_after'

# List of Python scripts to run
scripts = ['extract.py', 'list3.py', 'frequency.py', 'amino.py',
           'prob.py', 'entropy2.py', 'extseq.py', 'difference.py']

# Loop through each item in the main directory
for item in os.listdir(main_directory):
    # Construct the full path
    path = os.path.join(main_directory, item)
    
    # Check if the item is a directory
    if os.path.isdir(path):
        # If it is a directory, run each script sequentially for this subdirectory
        for script in scripts:
            # Construct the full path to the script
            script_path = os.path.join(main_directory, script)
            
            # Run the script using subprocess, setting the current working directory to 'path'
            print(f"Starting {script} in {path}...")
            subprocess.run(['python3', script_path], cwd=path, check=True)
            print(f"Completed {script} in {path}.")

print("Completed processing all scripts in all subdirectories.")
