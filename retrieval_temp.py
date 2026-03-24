# retrivaltemp.py
import os
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")

def retrieve_documents(query, top_k=3):
    """
    Retrieve top_k relevant visa documents based on query.
    Creates FAISS index if it doesn't exist.
    """
    # Check if FAISS index exists
    if not os.path.exists("faiss_index"):
        print("FAISS index not found. Creating new index...")
        countries = ["USA", "Canada", "UK", "Germany", "France", "Australia", "New Zealand",
                     "Japan", "Singapore", "Netherlands", "Sweden", "Switzerland", "Italy", "Ireland"]
        visa_types = ["Student Visa", "Work Visa", "Family Visa"]
        visa_docs = []

        for country in countries:
            for visa in visa_types:
                content = f"{country} {visa}: Description and requirements for {visa.lower()}."
                visa_docs.append(Document(page_content=content, metadata={"country": country, "visa_type": visa}))

        # Create FAISS vector store and save
        db = FAISS.from_documents(visa_docs, embedding_model)
        db.save_local("faiss_index")
        print("FAISS index created!")
    else:
        db = FAISS.load_local("faiss_index", embedding_model)

    # Perform similarity search
    results = db.similarity_search(query, k=top_k)
    return results
