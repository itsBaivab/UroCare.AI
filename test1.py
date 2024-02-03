import os
import pymongo
from llama_index import VectorStoreIndex, StorageContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection URL from environment variables
mongo_url = os.getenv("MONGO_URL")

# Connect to MongoDB
client = pymongo.MongoClient(mongo_url)

# Access the existing vector store
store = MongoDBAtlasVectorSearch(client)

# Create a storage context with the existing store
storage_context = StorageContext.from_defaults(vector_store=store)

# Load the existing index
index = VectorStoreIndex.load(storage_context)

# Ask queries and get responses
while True:
    query = input("Enter your query (or type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)