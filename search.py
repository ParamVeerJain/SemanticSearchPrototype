import streamlit as st
import pandas as pd
# Import the required functions
import llmRefine
import SemanticSearch
import imageCaption

# Define functions for text and image search
def textSearch(query):
    refined_query = llmRefine.getQuery(query)
    print(refined_query)
    results = SemanticSearch.query_faiss(refined_query)
    return results[['productDisplayName', 'averageRating', 'numberOfRatings', 'price', 'productId']].to_dict(orient='records')

def imageSearch(image_path):
    query = imageCaption.getImageCaptions(image_path)
    results = SemanticSearch.query_faiss(query)
    return results[['productDisplayName', 'averageRating', 'numberOfRatings', 'price', 'productId']].to_dict(orient='records')

# Main Streamlit app
def main():
    st.title("Semantic Search Prototype")

    # Selection for query type
    search_type = st.sidebar.selectbox("Choose Search Type", ("Text Search", "Image Search"))

    if search_type == "Text Search":
        # Text input for the search query
        query = st.text_input("Enter your search query:")
        if st.button("Search"):
            if query:
                results = textSearch(query)
                if results:
                    st.subheader("Search Results")
                    for result in results:
                        st.write(f"**Product Name:** {result['productDisplayName']}")
                        st.write(f"**Average Rating:** {result['averageRating']}")
                        st.write(f"**Number of Ratings:** {result['numberOfRatings']}")
                        st.write(f"**Price:** {result['price']}")
                        st.write(f"**Product ID:** {result['productId']}")
                        st.write("---")
                else:
                    st.write("No results found.")
            else:
                st.write("Please enter a query.")

    elif search_type == "Image Search":
        # File uploader for image
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            # To read file as bytes:
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
            if st.button("Search"):
                with open("temp_image.png", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                results = imageSearch("temp_image.png")
                if results:
                    st.subheader("Search Results")
                    for result in results:
                        st.write(f"**Product Name:** {result['productDisplayName']}")
                        st.write(f"**Average Rating:** {result['averageRating']}")
                        st.write(f"**Number of Ratings:** {result['numberOfRatings']}")
                        st.write(f"**Price:** {result['price']}")
                        st.write(f"**Product ID:** {result['productId']}")
                        st.write("---")
                else:
                    st.write("No results found.")
        else:
            st.write("Please upload an image.")

if __name__ == "__main__":
    main()
# Hello