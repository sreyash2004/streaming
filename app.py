import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

st.markdown("""
<style>

/* ===== Background ===== */
.stApp {
    background: linear-gradient(rgba(230,240,255,0.9), rgba(230,240,255,0.9)),
    url("https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1");
    background-size: cover;
    background-attachment: fixed;
}

/* ===== Main Card ===== */
.block-container {
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.2);
}

/* ===== LABEL FIX (MOST IMPORTANT) ===== */
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #111827 !important;   /* DARK BLACK */
    font-weight: 600 !important;
    font-size: 15px !important;
}

/* ===== INPUT TEXT ===== */
input, .stSelectbox div {
    color: #111827 !important;
    font-weight: 500;
}

/* ===== INPUT BOX ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #F9FAFB !important;
    border: 2px solid #D1D5DB !important;
    border-radius: 10px !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    color: white;
    font-size: 16px;
    font-weight: bold;
    height: 50px;
    border-radius: 12px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: #F3F4F6;
    padding: 20px;
    border-left: 6px solid #2563EB;
    border-radius: 10px;
    color: black;
}

/* ===== SIDEBAR TEXT ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A8A, #2563EB);
    color: white;
}

section[data-testid="stSidebar"] * {
    color: white !important;
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
