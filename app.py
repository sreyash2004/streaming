import streamlit as st
from retrievalout import retrieve_documents
from prompt_builder import build_prompt
from llm import generate_response

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="SwiftVisa AI",
    page_icon="🌍",
    layout="wide"
)

# Session state
if "response" not in st.session_state:
    st.session_state.response = None

# ------------------------------
# STYLING
# ------------------------------
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
    background-color: #f5f7fb;
}

/* Title */
.main-title {
    background: linear-gradient(90deg, #1E40AF, #2563EB);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}

/* Result box */
.result-box {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# HEADER
# ------------------------------
st.markdown('<div class="main-title">🌍 SwiftVisa AI</div>', unsafe_allow_html=True)

st.markdown("⚠️ AI-powered visa eligibility assistant (Demo)")

# Sidebar
st.sidebar.title("📌 Instructions")
st.sidebar.info("""
- Fill all fields  
- Select correct visa type  
- This is a demo system  
""")

# ------------------------------
# FORM
# ------------------------------
st.header("📝 Applicant Details")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 1, 100, 25)
    country = st.text_input("Destination Country")
    visa_type = st.selectbox("Visa Type", ["Student Visa", "Work Visa", "Tourist Visa"])

with col2:
    education = st.selectbox("Education", ["High School", "Bachelor", "Master", "PhD"])
    funds = st.selectbox("Financial Proof", ["Yes", "No"])
    income = st.number_input("Income", 0)
    criminal = st.selectbox("Criminal Record", ["No", "Yes"])

# ------------------------------
# BUTTON ACTION
# ------------------------------
if st.button("🔍 Check Visa Eligibility", use_container_width=True):

    if not country:
        st.error("Please enter destination country")
    else:
        profile = {
            "Age": age,
            "Country": country,
            "Visa": visa_type,
            "Education": education,
            "Funds": funds,
            "Income": income,
            "Criminal Record": criminal
        }

        with st.spinner("Analyzing your profile..."):

            # Query for retrieval
            query = f"{visa_type} in {country}"

            docs = retrieve_documents(query)

            prompt = build_prompt(profile, docs)

            response = generate_response(prompt)

            st.session_state.response = response

# ------------------------------
# RESULT DISPLAY
# ------------------------------
if st.session_state.response:

    res = st.session_state.response

    st.header("📊 Final Decision")

    # Eligibility
    if "NOT ELIGIBLE" in res:
        st.error("❌ NOT ELIGIBLE")
    else:
        st.success("✅ ELIGIBLE")

    # Full response
    st.markdown("### 📄 AI Response")
    st.markdown(f'<div class="result-box">{res}</div>', unsafe_allow_html=True)

    # Reset
    if st.button("🔄 Reset"):
        st.session_state.response = None
        st.rerun()
