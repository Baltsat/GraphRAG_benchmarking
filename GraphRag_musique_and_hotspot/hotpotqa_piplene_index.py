import os
import subprocess
import shutil

# Define the paths

dataset = 'hotpotqa'

input_dir = f'./ragtest_{dataset}/input'
output_dir = f'./ragtest_{dataset}/output'
documents_dir = f'./documents_{dataset}'

# Ensure input and output directories exist
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# List all subdirectories in the documents directory
document_folders = [d for d in os.listdir(documents_dir) if os.path.isdir(os.path.join(documents_dir, d))]

# Loop through each folder in the documents directory
for folder in document_folders:
    # Define paths for the current folder
    folder_path = os.path.join(documents_dir, folder)

    # Clear the input directory
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    # Copy all files from the current folder to the input directory
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, os.path.join(input_dir, file))


    # Run the indexing pipeline
    subprocess.run(['python', '-m', 'graphrag.index', '--root', f'./ragtest_{dataset}'])

    # Find the most recently created directory in the output folder (which should be the one just created)
    latest_output_dir = max([os.path.join(output_dir, d) for d in os.listdir(output_dir)], key=os.path.getmtime)

    # Construct the new name for the directory
    new_output_dir = f"ragtest_{dataset}/output/{folder}"

    # Rename the directory
    os.rename(latest_output_dir, new_output_dir)

    print(f'Processed folder {folder} and renamed output directory to {new_output_dir}')

# Clean up the input directory after processing all folders
shutil.rmtree(input_dir)
os.makedirs(input_dir, exist_ok=True)