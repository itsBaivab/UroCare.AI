import os
import openai
import pymongo
from llama_index import VectorStoreIndex, SimpleDirectoryReader ,StorageContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.storage.storage_context import StorageContext
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get the API key and MongoDB connection URL from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
mongo_url = os.getenv("MONGO_URL")

# Connect to MongoDB
client = MongoClient(mongo_url)


#setup client
mongodb_client = pymongo.MongoClient(mongo_url)

if mongodb_client:
    print("Connected to MongoDB")
else:
    print("Could not connect to MongoDB")
# Create a new database and collection
store =  MongoDBAtlasVectorSearch(mongodb_client)
print(store)

Storage_Context = StorageContext.from_defaults(
    vector_store=store
)

documents = SimpleDirectoryReader("input").load_data()
index = VectorStoreIndex.from_documents(documents, storage_context = Storage_Context)
print(index)

#ask query

query_engine = index.as_query_engine()
response = query_engine.query("I have Left kidney hydronephrosis for six months, Upper segment stone in the left ureter,Mild mitral and tricuspid valve regurgitation observed in the echocardiogram.What is the best treatment?")
print(response) 