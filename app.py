# app.py
import streamlit as st
from retrievaltemp import retrieve_documents  # updated module name

st.title("SwiftVisa – AI-Based Visa Eligibility Screening Agent")

query = st.text_input("Enter your visa query:")

if st.button("Check Eligibility"):
    if query:
        results = retrieve_documents(query)
        for doc in results:
            st.write(f"**Country:** {doc.metadata['country']}")
            st.write(f"**Visa Type:** {doc.metadata['visa_type']}")
            st.write(f"**Details:** {doc.page_content}")
            st.write("---")
    else:
        st.warning("Please enter a query.")
