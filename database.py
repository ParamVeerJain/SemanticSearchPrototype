import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import pickle

# Load data
file_path = 'fashion_products.csv'
df = pd.read_csv(file_path)

# Initialize the model
model_name = 'all-mpnet-base-v2'
model = SentenceTransformer(model_name)

# Convert descriptions to embeddings
descriptions = df['description'].tolist()
embeddings = model.encode(descriptions)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save the FAISS index and dataframe to disk
faiss.write_index(index, 'faiss_index.bin')
with open('products_dataframe.pkl', 'wb') as f:
    pickle.dump(df, f)

print("FAISS index and dataframe have been saved successfully.")
