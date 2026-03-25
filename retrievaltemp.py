import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def retrieve_documents(query, top_k=3):

    if not os.path.exists("faiss_index"):

        countries = ["USA", "Canada", "UK", "Germany", "France", "Australia"]
        visa_types = ["Student Visa", "Work Visa", "Tourist Visa"]

        docs = []

        for country in countries:
            for visa in visa_types:
                content = f"{country} {visa}: Basic requirements."
                docs.append(
                    Document(
                        page_content=content,
                        metadata={"country": country, "visa_type": visa}
                    )
                )

        db = FAISS.from_documents(docs, embedding_model)
        db.save_local("faiss_index")

    else:
        db = FAISS.load_local(
            "faiss_index",
            embedding_model,
            allow_dangerous_deserialization=True
        )

    return db.similarity_search(query, k=top_k)
