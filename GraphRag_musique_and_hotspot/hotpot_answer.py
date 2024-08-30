import os
import json
import shutil
import subprocess

dataset = 'hotpotqa'

# Paths
original_ragtest_dir = f'./ragtest_{dataset}'
output_dir = os.path.join(original_ragtest_dir, 'output')
temp_ragtest_dir = f'./ragtest_{dataset}_temp'
json_file_path = 'hotpotqa200.json'

# Load the questions from the JSON file
with open(json_file_path, 'r') as f:
    questions_data = json.load(f)

# Iterate over each question entry
for i, question_entry in enumerate(questions_data):
    #print("trial #", i)
    #if i <= 161:
    #    continue
    specific_output_folder = question_entry['_id']  # Accessing the ID field from the new structure

    # Find the corresponding question
    question = question_entry['question']  # Accessing the question field

    # Define the folder path
    specific_folder_path = os.path.join(output_dir, specific_output_folder)

    if not os.path.exists(specific_folder_path):
        print(f"Folder {specific_output_folder} does not exist, skipping...")
        continue

    # Clean up or create the temporary directory
    if os.path.exists(temp_ragtest_dir):
        shutil.rmtree(temp_ragtest_dir)
    os.makedirs(temp_ragtest_dir)

    # Copy all contents of ragtest except the output folder
    for item in os.listdir(original_ragtest_dir):

        s = os.path.join(original_ragtest_dir, item)
        d = os.path.join(temp_ragtest_dir, item)
        if os.path.isdir(s) and item == 'output':
            os.makedirs(d)  # Create the output directory
            # Copy only the specified output folder
            shutil.copytree(specific_folder_path, os.path.join(d, specific_output_folder))
        elif os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # Run the query command using the temporary directory
    result = subprocess.run(
        ['python', '-m', 'graphrag.query', '--root', temp_ragtest_dir, '--method', 'local', question],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    # Prepare the JSON response
    new_response_data = {
        "specific_output_folder": specific_output_folder,
        "question": question,
        "response": result.stdout.strip()
    }

    # Define the JSON file path to save the results
    output_json_path = os.path.join(original_ragtest_dir, f"response_{dataset}.json")

    # Check if the JSON file exists
    if os.path.exists(output_json_path):
        # Load existing data
        with open(output_json_path, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        # Start with an empty list if the file doesn't exist
        existing_data = []

    # Append the new response to the existing data
    existing_data.append(new_response_data)

    # Save the updated data back to the JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"Response appended to {output_json_path} for folder {specific_output_folder}")

    # Optionally, clean up the temporary directory afterward
    shutil.rmtree(temp_ragtest_dir)
