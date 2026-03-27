import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

st.markdown("""
<style>

/* ===== BACKGROUND (SOFT PREMIUM GRADIENT) ===== */
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f0f9ff, #eef2ff);
}

/* ===== MAIN CARD ===== */
.block-container {
    background: #ffffff;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* ===== TITLE ===== */
.main-title {
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    color: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* ===== LABELS ===== */
label {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 15px;
}

/* ===== INPUT BOX ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5f5 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}

/* Dropdown text */
.stSelectbox div[data-baseweb="select"] span {
    color: #0f172a !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background: white !important;
    color: black !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #3B82F6, #06B6D4);
    color: white;
    font-weight: bold;
    height: 50px;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(59,130,246,0.3);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: #f1f5f9;
    padding: 20px;
    border-left: 6px solid #3B82F6;
    border-radius: 10px;
    color: #0f172a;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2563EB, #38BDF8);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== REMOVE HEADER ===== */
header {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.title("⚠️ Important Notice")

st.sidebar.warning("""
This is an AI-based visa eligibility prediction system.

- This tool provides **guidance only**
- It does NOT guarantee visa approval
- Final decisions are made by official immigration authorities
- Always verify with embassy or official portals
""")

st.sidebar.info("""
✔ Designed for educational purposes  
✔ Uses simplified eligibility rules  
✔ Future version will include real-time policy updates  
""")

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Eligibility Checker</div>', unsafe_allow_html=True)

st.markdown("## 📝 Applicant Details")

# ===== FORM =====
name = st.text_input("Full Name")

age = st.number_input("Age", min_value=0, max_value=100)

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Select Country", [
        "", "USA", "Canada", "UK", "Australia", "Germany",
        "France", "Japan", "Singapore"
    ])
    visa_type = st.selectbox("Visa Type", ["", "Tourist", "Student", "Work"])
    education = st.selectbox("Education Level", ["", "High School", "Bachelor", "Master", "PhD"])

with col2:
    criminal_record = st.selectbox("Criminal Record", ["", "No", "Yes"])
    purpose = st.selectbox("Purpose of Visit", ["Tourism", "Study", "Work"])
    annual_income = st.number_input("Annual Income ($)", min_value=0)
    financial_proof = st.selectbox("Financial Proof Available", ["Yes", "No"])

# ===== BUTTON =====
if st.button("Check Eligibility"):

    # ===== VALIDATION =====
    if (
        age == 0 or
        country == "" or
        visa_type == "" or
        criminal_record == "" or
        education == ""
    ):
        st.error("⚠️ Please fill all mandatory fields (Age, Country, Visa Type, Criminal Record, Education)")
    
    else:
        with st.spinner("Analyzing your application... ⏳"):
            result, reason = retrieve_documents(age, country, visa_type)

        # ===== RESULT =====
        if result == "Eligible":
            st.balloons()
            st.success("🎉 Congratulations! You are Eligible!")
        else:
            st.error("❌ Sorry, You are Not Eligible")

        st.markdown(f"""
        <div class="result-box">
        {reason}
        </div>
        """, unsafe_allow_html=True)
        
