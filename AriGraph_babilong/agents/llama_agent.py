import transformers
from huggingface_hub import snapshot_download
import torch
import requests
from time import sleep
from langchain_ollama import ChatOllama
from agents.parent_agent import GPTagent
model = ChatOllama(
    model="llama3.1:70b-instruct-q6_K", temperature=0,
)


class LLaMAagent(GPTagent):  # assuming GPTagent is the parent class
    def __init__(self, system_prompt, model):
        self.system_prompt = system_prompt
        self.model = model
        # Call the superclass init method correctly
        # self.pipeline = transformers.pipeline(
        #     "text-generation",
        #     model = './models/llama-7b-hf',
        #     # model="Undi95/Meta-Llama-3-8B-Instruct-hf",
        #     model_kwargs={"torch_dtype": torch.bfloat16},
        #     device_map="auto"
        # ) if pipeline is None else pipeline
        
    def generate(self, prompt, jsn = False, t = 0.2):
        messages = [
                ("system", self.system_prompt),
                ("human", prompt),
            ]
        
        response_message = model.invoke(messages)
        outputs = response_message.content
        
        
        print(outputs)
        
        return outputs, 0