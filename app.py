import streamlit as st
from retrievaltemp import retrieve_documents

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="SwiftVisa AI",
    page_icon="🌍",
    layout="wide"
)

# ------------------------------
# TITLE
# ------------------------------
st.title("🌍 SwiftVisa – AI-Based Visa Eligibility Screening Agent")

st.write("""
Enter a visa-related query to retrieve relevant country and visa information.
""")

# ------------------------------
# INPUT
# ------------------------------
query = st.text_input("🔍 Enter your visa query:")

# ------------------------------
# BUTTON ACTION
# ------------------------------
if st.button("Check Eligibility"):

    if query:
        results = retrieve_documents(query)

        if results:
            st.success("✅ Results Found")

            for doc in results:
                st.markdown(f"""
                **🌎 Country:** {doc.metadata.get('country', 'N/A')}  
                **🛂 Visa Type:** {doc.metadata.get('visa_type', 'N/A')}  

                **📄 Details:**  
                {doc.page_content}
                """)
                st.write("---")
        else:
            st.warning("No matching visa information found.")

    else:
        st.warning("Please enter a query.")
