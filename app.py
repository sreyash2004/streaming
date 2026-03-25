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
st.markdown("""
<style>

/* ===== BACKGROUND IMAGE (PERFECT BALANCE) ===== */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)),
    url("https://images.unsplash.com/photo-1526779259212-756e4dcd2e38");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Hide default */
header {visibility: hidden;}
footer {visibility: hidden;}

/* ===== TITLE ===== */
.main-title {
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    animation: fadeInDown 1s ease-in-out;
}

/* ===== CONTAINER ===== */
.block-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.15);
}

/* ===== LABELS (FORCE DARK) ===== */
label, .stMarkdown, .stText, .stSelectbox label {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* ===== INPUT TEXT ===== */
input, textarea {
    color: #111827 !important;
}

/* ===== INPUT FIELDS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5f5 !important;
    padding: 10px !important;
}

/* Fix dropdown text */
.stSelectbox div[data-baseweb="select"] span {
    color: #111827 !important;
}

/* Focus */
.stTextInput input:focus,
.stNumberInput input:focus {
    border: 1px solid #2563EB !important;
    box-shadow: 0 0 8px rgba(37, 99, 235, 0.4);
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #2563EB, #1E40AF);
    color: white;
    font-weight: bold;
    border-radius: 14px;
    height: 52px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(37,99,235,0.4);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: #ffffff;
    color: #111827;
    padding: 22px;
    border-radius: 14px;
    border-left: 6px solid #2563EB;
    font-size: 17px;
    line-height: 1.7;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.95);
}

section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeInDown {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
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
