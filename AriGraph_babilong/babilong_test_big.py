import json
import torch
import numpy as np
import transformers
import os

from graphs.contriever_graph import LLaMAContrieverGraph, ContrieverGraph
from agents.llama_agent import LLaMAagent
from agents.parent_agent import GPTagent
from utils.utils import Logger
from langchain_ollama import ChatOllama

# musique | hotpotqa | babilong
task_name = "babilong"

context_lengths = ['0k', '4k', '8k', '16k', '32k', '64k', '128k', '256k', '512k', '1M']
# context_lengths = ['0k', '4k']
# context_lengths = ['4k', '32k', '64k', '128k', '256k', '512k', '1M']
topk_episodic = 2
graph_model, qa_model = "llama", "llama"
N_task_to_try = 10

def run(context_length):
    log_path = f"chunking_{task_name}_{N_task_to_try}_testLlamaOllama_{context_length}"
    log = Logger(log_path)
    
    tasks = get_data(task_name, context_length)
    print('='*50, tasks [:1], '='*50)
    agent_items, agent_qa, graph = load_setup(graph_model, qa_model)
    trueP, pred_len, true_len, EM = [], [], [], []
    
    completed_tasks = 0
    for task in tasks:
        if completed_tasks >= N_task_to_try:
            break
        
        try:
            graph.clear()
            for text in task["paragraphs"]:
                triplets, episodic = graph.update_without_retrieve(text["paragraph_text"], [], log)
            question = task["question"]
            log("-" * 15)
            log("QUESTION: " + str(question))
            items_list = agent_items.item_processing_scores_qa(question)
            if not items_list or not isinstance(items_list[0], dict):
                raise ValueError("INCORRECT FORMAT OF ITEMS: " + str(items_list))
            items = items_list[0]
            log("CRUCIAL ITEMS: " + str(items))

            subgraph, episodic = graph.retrieve(items, question, [], topk_episodic)
            log("ASSOCIATED SUBGRAPH: " + str(subgraph))
            log("EPISODIC MEMORY: " + str(episodic))

            answer_list = get_answer(agent_qa, question, subgraph, episodic)
            if not answer_list:
                raise ValueError("ERROR: No answer generated")
            answer = answer_list[0]
            log("AGENT ANSWER: " + str(answer))
            log("TRUE ANSWER: " + str(task["answer"]))
            compute_and_accumulate_metrics(answer, task, trueP, true_len, pred_len, EM, log)
            log("="* 56 + "\n")
            
            completed_tasks += 1
        except Exception as e:
            log(f"Error processing task: {e}")
            continue

    # Compute and log final metrics
    final_metrics = compute_final_metrics(trueP, pred_len, true_len, EM)
    log(f"Final Metrics: {final_metrics}")

from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_data(task_name, context_length):
    if task_name == "musique":
        with open('qa_data/musique_ans_v1.0_dev.jsonl', 'r') as json_file:
            json_list = list(json_file)
        tasks = []
        for json_str in json_list:
            result = json.loads(json_str)
            tasks.append(result)

    if task_name == "hotpotqa":
        with open('qa_data/hotpot_dev_distractor_v1.json', 'r') as inp:
            data = json.load(inp)
        tasks = [" ".join(task["context"][-1]) for task in data]
        
    if task_name == 'babilong':
        # Define the paths
        documents_dir = f'graphrag_babilong_data/qa1/documents_babilong_{context_length}'
        json_file_path = f'graphrag_babilong_data/qa1/babilong_{context_length}.json'

        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        combined_data = []

        # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,  # Adjust chunk size as needed
            chunk_overlap=50,  # Adjust overlap as needed
            length_function=len,
            separators=["\n\n", "\n", '.', ' ', ''], #Note: The split first happens at “\n\n”, if the chunk size exceeds, it will move to the next separator, if it still exceeds, it will move to the next separator which is “ “ and so on.
        )

        # Traverse through the documents directory
        for subdir, _, files in os.walk(documents_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(subdir, file)
                    with open(file_path, 'r', encoding='utf-8') as txt_file:
                        paragraph_text = txt_file.read()
                    
                    # Split the text into chunks
                    chunks = text_splitter.split_text(paragraph_text)

                    # Extract the subfolder name and match it with the JSON data
                    subfolder_name = os.path.basename(subdir)
                    json_entry = next((entry for entry in json_data if entry['_id'] == subfolder_name), None)
                    
                    if json_entry:
                        paragraphs = [{
                            'idx': i,
                            'title': subfolder_name,
                            'paragraph_text': chunk,
                            'is_supporting': True
                        } for i, chunk in enumerate(chunks)]

                        combined_entry = {
                            'id': subfolder_name,
                            'paragraphs': paragraphs,
                            'question': json_entry['question'],
                            'question_decomposition': [],
                            'answer': json_entry['answer'],
                            'answer_aliases': [],
                            'answerable': True
                        }
                        combined_data.append(combined_entry)
        tasks = combined_data

    ids = np.random.RandomState(seed=42).permutation(len(tasks))[:2*N_task_to_try]
    tasks = [tasks[i] for i in ids]
    return tasks

def get_answer(agent, question, subgraph, episodic):
    prompt = f'''Your task is answer the following question: "{question}"

    Relevant facts from your memory: {subgraph}

    Relevant texts from your memory: {episodic}

    Answer the question "{question}" with Chain of Thoughts in the following format:
    "CoT: your chain of thoughts
    Direct answer: your direct answer to the question"
    Direct answer must be concrete and must not contain alternatives, descriptions or reasoning.
    Write "Unknown" if you have doubts.
    Do not write anything except answer in the given format.

    Your answer: '''
    return agent.generate(prompt)

def compute_and_accumulate_metrics(answer, task, trueP, true_len, pred_len, EM, log):
    answer = answer.split("Direct answer:")[-1].strip('''. \n`'"?''').lower().split()
    answer = [el.strip('''. \n'`"?''') for el in answer]
    true_answer = task["answer"].strip('''. \n'`"?''').lower().split()
    true_answer = [el.strip('''. \n'`"?''') for el in true_answer]
    true_P = len({word for word in answer if word in true_answer})
    trueP.append(true_P), pred_len.append(len(answer)), true_len.append(len(true_answer))
    EM.append(answer == true_answer)

def compute_final_metrics(trueP, pred_len, true_len, EM):
    prec = np.sum(trueP) / np.sum(pred_len) if np.sum(pred_len) > 0 else 0
    rec = np.sum(trueP) / np.sum(true_len) if np.sum(true_len) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    em = np.mean(EM)
    return {"F1": f1, "RECALL": rec, "PRECISION": prec, "EXACT MATCH": em}

def load_setup(graph_model, qa_model):
    pipeline = ''
    if "llama" in graph_model:
        graph = LLaMAContrieverGraph("", "You are a helpful assistant", "", pipeline, "cuda")
        agent_items = LLaMAagent("You are a helpful assistant", pipeline)

    else:
        graph = ContrieverGraph(graph_model, "You are a helpful assistant", "YOUR KEY HERE", "cuda")
        agent_items = GPTagent(graph_model, "You are a helpful assistant", "YOUR KEY HERE")

    if "llama" in qa_model:
        agent_qa = LLaMAagent("You are a helpful assistant", pipeline)

    else:
        agent_qa = GPTagent(graph_model, "You are a helpful assistant", "YOUR KEY HERE")

    return agent_items, agent_qa, graph

if __name__ == "__main__":
    for context_length in context_lengths:
        try:
            run(context_length)
        except Exception as e:
            log_path = f"{task_name}_testLlamaOllama_{context_length}"
            log = Logger(log_path)
            log(f"Error for running on {context_length}: {e}")
            continue