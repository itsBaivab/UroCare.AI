import os
from pymongo import MongoClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import mongodb_atlas
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI



# Load environment variables from .env file
load_dotenv()


# Define the URL of the PDF MongoDB Atlas Best Practices document

# Retrieve environment variables for sensitive information
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

ATLAS_CONNECTION_STRING = os.getenv('ATLAS_CONNECTION_STRING')
if not ATLAS_CONNECTION_STRING:
    raise ValueError("The ATLAS_CONNECTION_STRING environment variable is not set.")

# Connect to MongoDB Atlas cluster using the connection string
cluster = MongoClient(ATLAS_CONNECTION_STRING)

# Define the MongoDB database and collection names
DB_NAME = "vectordatabase"
COLLECTION_NAME = "vector_collection"

# Connect to the specific collection in the database
MONGODB_COLLECTION = cluster[DB_NAME][COLLECTION_NAME]

# Initialize the PDF loader with the defined URL
path = "D:\\Urologist.AI\\test"  # Fix the path string by escaping the backslashes
loader = TextLoader("test\input2.txt", encoding = 'UTF-8')

data = loader.load()
print(len(data))

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

# Split the document into manageable segments
docs = text_splitter.split_documents(data)

# code for ingesting the documents into MongoDB Atlas -----------------------------------------
# Initialize MongoDB Atlas vector search with the document segments
# vector_search = mongodb_atlas.MongoDBAtlasVectorSearch.from_documents(
#     documents=docs,
#     embedding=OpenAIEmbeddings(disallowed_special=()),
#     collection=MONGODB_COLLECTION,
#     index_name="vector_index"  # Use a predefined index name
# )
# -------------------------------------------------------------------------------------------
# code for searching the documents in MongoDB Atlas -----------------------------------------
vector_search = mongodb_atlas.MongoDBAtlasVectorSearch.from_connection_string(
    ATLAS_CONNECTION_STRING,
    DB_NAME + "." + COLLECTION_NAME,
    OpenAIEmbeddings(disallowed_special=()),
    index_name="vector_index"
)
# -------------------------------------------


# CREATEING A RETRIEVAL QA CHAIN -----------------------------------------
qa_retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2},
)

prompt_template = """You are a Urologist Doctor who provides friendly assistance and helps to diagnose patients and suggest them treatment . Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.Always give the answers in english language.
Traslate the context to english language before using it to answer the question.also Traslate the question in english language before using it with the context to answer .

Context: {context}

Question: {question}
Only return the helpful answer below and nothing else.

Helpful answer(must be in english language):
"""


PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)


# print(docs["source_documents"])
import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/d30b1e8a5bd36620f3710b178f5f9673/ai/run/"
headers = {"Authorization": "Bearer Vb8tymIOp_0pJDawvLQ634Y_z7yzOvkzJumR1me7"}

def run(model, input):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()
# input = """Pain: The patient experiences renal colic, often intermittent and radiating to the perineum. In chronic cases, pain may be less prominent.Urinary Symptoms: Bilateral incomplete obstruction may result in polyuria, while complete obstruction may lead to anuria. Infection-related obstructions may cause bladder irritation symptoms. Hypertension: Common due to increased renin secretion or sodium retention. Polycythemia: Due to increased erythropoietin secretion from hydronephrosis. Acidosis: Impaired renal tubular acid secretion.. GIVE ME SOME ADICE ON TREATMENT OPTIONS alsway give"""


output = run('@cf/meta/m2m100-1.2b', {
    "text": " bilateral ureteral stones is causing obstruction, leading to hydronephrosis and impaired urine flow.Give me some treatment suggestions",
    "source_lang": "english",
    "target_lang": "chinese"
})
# print(output["result"]["translated_text"])
docs = qa({"query": output["result"]["translated_text"]})

if docs["result"]:
    print(docs["result"])
# print(docs["result"]) 
# print(output)



