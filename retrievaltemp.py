import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ------------------------------
# EMBEDDING MODEL
# ------------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ------------------------------
# RETRIEVE DOCUMENTS
# ------------------------------
def retrieve_documents(query, top_k=3):

    # If index does NOT exist → create it
    if not os.path.exists("faiss_index"):

        print("Creating FAISS index...")

        countries = [
            "USA", "Canada", "UK", "Germany", "France",
            "Australia", "New Zealand", "Japan", "Singapore",
            "Netherlands", "Sweden", "Switzerland", "Italy", "Ireland"
        ]

        visa_types = ["Student Visa", "Work Visa", "Tourist Visa"]

        visa_docs = []

        for country in countries:
            for visa in visa_types:
                content = f"{country} {visa}: Basic requirements and general information."
                
                visa_docs.append(
                    Document(
                        page_content=content,
                        metadata={
                            "country": country,
                            "visa_type": visa
                        }
                    )
                )

        # Create FAISS DB
        db = FAISS.from_documents(visa_docs, embedding_model)

        # Save index
        db.save_local("faiss_index")

        print("FAISS index created successfully!")

    else:
        # Load existing index
        db = FAISS.load_local(
            "faiss_index",
            embedding_model,
            allow_dangerous_deserialization=True   # REQUIRED for newer versions
        )

    # Perform search
    results = db.similarity_search(query, k=top_k)

    return results
