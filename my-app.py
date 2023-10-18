import inspect
import os
import json 

from dotenv import load_dotenv

from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams
from langchain.document_loaders import PyPDFLoader


# make sure you have a .env file under genai root with
# GENAI_KEY=<your-genai-key>
# GENAI_API=<genai-api-endpoint>
load_dotenv()
api_key = os.getenv("GENAI_KEY", None)
api_endpoint = os.getenv("GENAI_API", None)

print("\n------------- Example (Complete my code)-------------\n")

params = GenerateParams(
    decoding_method="sample",
    max_new_tokens=1024,
    min_new_tokens=1,
    stream=False,
    temperature=0.7,
    top_k=50,
    top_p=1,
)

creds = Credentials(api_key, api_endpoint)


# # pass in an actual python function to explain
# #def add_numbers(number_one, number_two):
# #    return number_one

# read pdf file
pdf_path = "path-to-pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()
context = ""
context_list=[]
for page_number in range(len(pages)):
   # context = print(pages[page_number].page_content)
   context = str(pages[page_number].page_content)+"\n"+"can you generate some possible questions a client might ask from this text?"
   context_list.append(context)

# Instantiate parameters for text generation
params = GenerateParams(decoding_method="sample", max_new_tokens=1024)

# Instantiate a model proxy object to send your requests
llama_chat = Model("meta-llama/llama-2-70b-chat", params=params, credentials=creds)


#context+'\n'+
# prompts = [context+"\n"+"can you generate some possible questions a client might ask from this text?"]
index = 1
dictionary = {index:""}

# # Call generate function
responses = llama_chat.generate_as_completed(context_list)
for response in responses:
    print(f"Generated text: {response.generated_text}")



	
# Data to be written
	
with open("sampl.json", "w") as outfile:
	json.dump(dictionary, outfile)