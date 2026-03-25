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

/* ===== BACKGROUND (GRADIENT + SOFT LOOK) ===== */
.stApp {
    background: linear-gradient(135deg, #dbeafe, #f0f9ff);
}

/* Hide default Streamlit UI */
header {visibility: hidden;}
footer {visibility: hidden;}

/* ===== MAIN TITLE ===== */
.main-title {
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

/* ===== SECTION HEADINGS (FIXED VISIBILITY) ===== */
h1, h2, h3 {
    color: #1E293B !important;
    font-weight: 700 !important;
}

/* ===== CARD CONTAINER ===== */
.block-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

/* ===== LABELS (CLEAR & DARK) ===== */
label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #0f172a !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* ===== INPUT FIELDS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 10px !important;
    border: 1px solid #cbd5f5 !important;
    padding: 10px !important;
    transition: 0.3s;
}

/* Focus glow */
.stTextInput input:focus,
.stNumberInput input:focus,
.stSelectbox div[data-baseweb="select"]:focus-within {
    border: 1px solid #2563EB !important;
    box-shadow: 0 0 8px rgba(37, 99, 235, 0.4);
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #2563EB, #1E40AF);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 50px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(37,99,235,0.4);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: white;
    color: #111827;
    padding: 22px;
    border-radius: 14px;
    border-left: 6px solid #2563EB;
    font-size: 17px;
    line-height: 1.8;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* ===== ALERT TEXT (MAKE VISIBLE) ===== */
.stAlert {
    color: #111827 !important;
    font-weight: 600;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e0ecff, #f8fafc);
}

section[data-testid="stSidebar"] * {
    color: #0f172a !important;
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
