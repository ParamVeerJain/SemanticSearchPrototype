import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import pickle
import llmRefine

# Load the saved FAISS index and dataframe
index = faiss.read_index('faiss_index.bin')
with open('products_dataframe.pkl', 'rb') as f:
    df = pickle.load(f)

# Initialize the model
model_name = 'all-mpnet-base-v2'
model = SentenceTransformer(model_name)

# Function to query the FAISS database
def query_faiss(query, top_k=30):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    
    results = df.iloc[indices[0]].reset_index(drop=True)
    return results[['productDisplayName', 'averageRating', 'numberOfRatings', 'price','productId']]
