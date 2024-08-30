import json
import re
import numpy as np


# Function to remove ANSI escape codes
def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


# Load JSON files
with open('ragtest_hotpotqa/response_hotpotqa.json', 'r') as f:
    model_responses = json.load(f)

with open('hotpotqa200.json', 'r') as f:
    true_answers_data = json.load(f)

# Create dictionaries for quick lookup
true_answers_dict = {item['_id']: item['answer'] for item in true_answers_data}

# Initialize metrics lists
trueP = []
pred_len = []
true_len = []
EM = []


# Define logging function
def log(message):
    print(message)


# Process each model response
for item in model_responses:
    specific_output_folder = item["specific_output_folder"]
    response = item["response"]

    # Remove ANSI escape codes
    response_clean = remove_ansi_escape_codes(response)

    # Extract answer from cleaned response
    answer = response_clean.split("Direct answer:")[-1].strip('''. \n`'"?''').lower().split()
    answer = [el.strip('''. \n'`"?''') for el in answer]

    print("answer", answer)

    # Get the true answer and clean it
    true_answer = true_answers_dict.get(specific_output_folder, '')
    true_answer_clean = remove_ansi_escape_codes(true_answer).strip('''. \n'`"?''').lower().split()
    true_answer_clean = [el.strip('''. \n'`"?''') for el in true_answer_clean]

    print('true answer', true_answer)

    # Calculate true positives
    true_P = len({word for word in answer if word in true_answer_clean})
    trueP.append(true_P)
    pred_len.append(len(answer))
    true_len.append(len(true_answer_clean))

    # Exact match
    EM.append(answer == true_answer_clean)

# Calculate precision, recall, and F1 score
if np.sum(pred_len) > 0:
    prec = np.sum(trueP) / np.sum(pred_len)
else:
    prec = 0.0

if np.sum(true_len) > 0:
    rec = np.sum(trueP) / np.sum(true_len)
else:
    rec = 0.0

if (prec + rec) > 0:
    f1 = 2 * prec * rec / (prec + rec)
else:
    f1 = 0.0

em = np.mean(EM)

# Print metrics
log(f"Mean F1 Score: {f1:.4f}")
log(f"Mean Exact Match (EM): {em:.4f}")
log("=" * 56 + "\n")
