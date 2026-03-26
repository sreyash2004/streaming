import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(rgba(20,30,60,0.75), rgba(20,30,60,0.75)),
    url("https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1");
    background-size: cover;
    background-attachment: fixed;
}

/* ===== MAIN CARD ===== */
.block-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* ===== TITLE FIX ===== */
.main-title {
    background: linear-gradient(90deg, #06B6D4, #3B82F6);
    color: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 20px;
    letter-spacing: 1px;
}

/* ===== LABELS ===== */
label {
    color: #E5E7EB !important;
    font-weight: 600 !important;
    font-size: 15px;
}

/* ===== INPUT TEXT ===== */
input {
    color: #111827 !important;
}

/* ===== INPUT BOX ===== */
.stTextInput input,
.stNumberInput input {
    background: #F9FAFB !important;
    border-radius: 10px !important;
}

/* ===== SELECT BOX FIX (IMPORTANT) ===== */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1F2937 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* Selected text */
.stSelectbox div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: #111827 !important;
    color: white !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #06B6D4, #3B82F6);
    color: white;
    font-weight: bold;
    height: 52px;
    border-radius: 12px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: rgba(255,255,255,0.1);
    color: white;
    padding: 20px;
    border-left: 6px solid #06B6D4;
    border-radius: 10px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #1E3A8A);
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

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
