# GraphRAG_benchmarking
Benchmarking GraphRAG and Arigraph on Musique, HotpotQA and Babilong QA1 datasets locally using Ollama with LLama3.

# Benchmarking [GraphRAG](https://github.com/microsoft/graphrag) on Musique, HotpotQA 
**Credits**
- [TheAiSingularity/graphrag-local-ollama](https://github.com/TheAiSingularity/graphrag-local-ollama)
- [AIRI-Institute/AriGraph](https://github.com/AIRI-Institute/AriGraph)

## Problem
Retrieval-Augmented Generation (RAG) struggles to generate accurate answers to complex or “global” questions that require understanding the entire dataset, not just individual fragments. Traditional RAG approaches rely heavily on vector search, which often results in incomplete or misleading answers because it only considers the top-k most semantically similar text segments, missing the broader context and relationships within the data.

## Objective
Test approaches that can map and analyze contextual relationships between entities in a large dataset, capturing both direct and indirect relationships that provide a deeper understanding of the data structure and provide an answer by reflecting their roles and interactions in the broader context of the dataset.

## Results
### GraphRAG vs. AriGraph
| Метод | GraphRAG (GPT-4o-mini) | AriGraph (GPT-40-mini) | AriGraph wwwww (LLama-3-70B) | AriGraph (GPT-4) |
|-------|------------------------|------------------------|------------------------------|-------------------|
| **MuSiQue** |
| EM | 40.0 | 23.0 | 27.0 | 37.0 |
| F1 | <u>53.5</u> | 35.1 | 36.7 | 47.4 |
| **HotpotQA** |
| EM | 58.7 | 50.9 | 43.0 | 59.5 |
| F1 | 63.3 | 60.3 | 51.8 | <u>69.6</u> |

### AriGraph benchmarking (N=10) on Babilong QA1 dataset
| Metric\Context | 0k     | 4k     | 8k     | 16k    |
|-----------------|--------|--------|--------|--------|
| EM              | 0.615  | 0.5    | 0.3    | 0.3    |
| F1              | 0.675  | 0.5    | 0.3    | 0.3    |
*Exact Match = true answer is a subset of generated answer*

### Benchmarking results Llama-3-70B vs GPT-4o-mini с Microsoft GraphRAG
| Model         | HotpotQA |       | BABILong 0k |       | MuSiQue |       | BABILong 4k, 8k, 16k, 32k |       |
|---------------|----------|-------|--------------|-------|---------|-------|---------------------------|-------|
|               | EM       | F1    | EM           | F1    | EM      | F1    | EM                        | F1    |
| Local         | 18.0     | 33.7  | 8.7          | 2.1   | 69.2    | 67.2  | 0                         | 0     |
| Global        | 4.0      | 5.1   | 3.2          | 1.7   | 61.5    | 33.2  | 0                         | 0     |
| GPT-4o-mini   | 58.7     | 63.3  | 40.0         | 53.5  | -       | -     | -                         | -     |

### Benchmarking Llama-3-70B with Microsoft GraphRAG vs AriGraph
| Model    | HotpotQA |       | BABILong 0k |       | MuSiQue |       | BABILong 4k, 8k, 16k, 32k |       |
|----------|----------|-------|-------------|-------|---------|-------|---------------------------|-------|
|          | EM       | F1    | EM          | F1    | EM      | F1    | EM                        | F1    |
| Local    | 18.0     | 33.7  | 8.7         | 2.1   | 69.2    | 67.2  | 0                         | 0     |
| Global   | 4.0      | 5.1   | 3.2         | 1.7   | 61.5    | 33.2  | 0                         | 0     |
| Arigraph | 43.0     | 51.8  | 27.0        | 36.7  | 61.5    | 67.2  | 0.3                       | 0.3   |

### Full Online version of the report

[Google Docs](https://docs.google.com/document/d/1u8KYps1oAbqJuWYZ5v49LpA5oPJ1TUzRIqFm-11ygD8/edit#heading=h.vbkrpx3o7dwm)

![Graph showing benchmarking results](<images/Safari 12_32_59 30_August_2024.jpg>)


### 🤝 Contributing

**We welcome contributions from the community to help enhance GraphRAG Local Ollama! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get involved.**

Need support for llama integration.

## 🚀 GraphRAG Local Ollama - Knowledge Graph

Welcome to **GraphRAG Local Ollama**! This repository is an exciting adaptation of Microsoft's [GraphRAG](https://github.com/microsoft/graphrag), tailored to support local models downloaded using Ollama. Say goodbye to costly OpenAPI models and hello to efficient, cost-effective local inference using Ollama!

### 📄 Research Paper

For more details on the GraphRAG implementation, please refer to the [GraphRAG paper](https://arxiv.org/pdf/2404.16130).

**Paper Abstract**

The use of retrieval-augmented generation (RAG) to retrieve relevant information from an external knowledge source enables large language models (LLMs)to answer questions over private and/or previously unseen document collections.However, RAG fails on global questions directed at an entire text corpus, suchas "What are the main themes in the dataset?", since this is inherently a queryfocused summarization (QFS) task, rather than an explicit retrieval task. PriorQFS methods, meanwhile, fail to scale to the quantities of text indexed by typicalRAG systems. To combine the strengths of these contrasting methods, we proposea Graph RAG approach to question answering over private text corpora that scaleswith both the generality of user questions and the quantity of source text to be indexed. Our approach uses an LLM to build a graph-based text index in two stages:first to derive an entity knowledge graph from the source documents, then to pregenerate community summaries for all groups of closely-related entities. Given aquestion, each community summary is used to generate a partial response, beforeall partial responses are again summarized in a final response to the user. For aclass of global sensemaking questions over datasets in the 1 million token range,we show that Graph RAG leads to substantial improvements over a na¨ıve RAGbaseline for both the comprehensiveness and diversity of generated answers. 

### 🌟 Features

- **Local Model Support:** Leverage local models with Ollama for LLM and embeddings.
- **Cost-Effective:** Eliminate dependency on costly OpenAPI models.
- **Easy Setup:** Simple and straightforward setup process.

### 📦 Installation and Setup

Follow these steps to set up this repository and use GraphRag with local models provided by Ollama :


1. **Create and activate a new conda environment:  (please stick to the given python version 3.10 for no errors)**
    
    conda create -n graphrag-ollama-local python=3.10
    conda activate graphrag-ollama-local
    

2. **Install Ollama:**
    - Visit [Ollama's website](https://ollama.com/) for installation instructions.
    - Or, run:
    
    curl -fsSL https://ollama.com/install.sh | sh #ollama for linux
    pip install ollama
    

3. **Download the required models using Ollama, we can choose from (mistral,gemma2, qwen2) for llm and any embedding model provided under Ollama:**
    
    ollama pull mistral  #llm
    ollama pull nomic-embed-text  #embedding
    

4. **Clone the repository:**
    
    git clone https://github.com/TheAiSingularity/graphrag-local-ollama.git
    

5. **Navigate to the repository directory:**
    
    cd graphrag-local-ollama/
    

6. **Install the graphrag package ** This is the most important step :**
    
    pip install -e .
    


7. **Create the required input directory: This is where the experiments data and results will be stored - ./ragtest**
    
    mkdir -p ./ragtest/input
    
    
8. **Copy sample data folder input/  to  ./ragtest. Input/ has the sample data to run the setup. You can add your own data here in .txt format.**
    
    cp input/* ./ragtest/input
    
    
9. **Initialize the ./ragtest folder to create the required files:**
    
    python -m graphrag.index --init --root ./ragtest
    

10. **Move the settings.yaml file, this is the main predefined config file configured with ollama local models :**
    
    cp settings.yaml ./ragtest
    

Users can experiment by changing the models. The llm model expects language models like llama3, mistral, phi3, etc., and the embedding model section expects embedding models like mxbai-embed-large, nomic-embed-text, etc., which are provided by Ollama. You can find the complete list of models provided by Ollama here https://ollama.com/library, which can be deployed locally. The default API base URLs are http://localhost:11434/v1 for LLM and http://localhost:11434/api for embeddings, hence they are added to the respective sections. 

![LLM Configuration](<images/Code 01_40_51 30_August_2024.jpg>)

![Embedding Configuration](<images/Code 01_41_08 30_August_2024.jpg>) 

P.s. as it was noticed that the embeddings were not working with the default settings.yaml, the following changes were made to the settings.yaml file to make it work: https://github.com/TheAiSingularity/graphrag-local-ollama/issues/51#issuecomment-2308460607

11. **Run the indexing, which creates a graph:**
    
    python -m graphrag.index --root ./ragtest
    

12. **Run a query: Only supports Global method** 
    
    python -m graphrag.query --root ./ragtest --method global "What is machine learning?"
    

**Graphs can be saved which further can be used for visualization by changing the graphml to "true" in the settings.yaml :**
    
    snapshots:
    graphml: true
    
**To visualize the generated graphml files, you can use : https://gephi.org/users/download/ or the script provided in the repo visualize-graphml.py :**

Pass the path to the .graphml file to the below line in visualize-graphml.py:

    graph = nx.read_graphml('output/20240708-161630/artifacts/summarized_graph.graphml') 

13. **Visualize .graphml :**

    
    python visualize-graphml.py
    



## Citations

- GraphRAG-ollama-local: [GraphRAG-ollama-local](https://github.com/TheAiSingularity/graphrag-local-ollama)
- Original GraphRAG repository by Microsoft: [GraphRAG](https://github.com/microsoft/graphrag)
- Ollama: [Ollama](https://ollama.com/)

---

By following the above steps, you can set up and use local models with GraphRAG, making the process more cost-effective and efficient.



