import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

st.markdown("""
<style>

/* ===== BACKGROUND IMAGE ===== */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)),
    url("https://images.unsplash.com/photo-1526779259212-756e4dcd2e38");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

header {visibility: hidden;}
footer {visibility: hidden;}

.main-title {
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

.block-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.15);
}

label {
    color: #0f172a !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5f5 !important;
    padding: 10px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #2563EB, #1E40AF);
    color: white;
    font-weight: bold;
    border-radius: 14px;
    height: 52px;
}

.result-box {
    background: #ffffff;
    color: #111827;
    padding: 22px;
    border-radius: 14px;
    border-left: 6px solid #2563EB;
}

</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Eligibility Checker</div>', unsafe_allow_html=True)

st.markdown("## 📝 Applicant Details")

# ===== FORM =====
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=100)

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Select Country", [
        "USA", "Canada", "UK", "Australia", "Germany",
        "France", "Japan", "UAE", "Singapore", "India"
    ])
    visa_type = st.selectbox("Visa Type", ["Tourist", "Student", "Work"])
    education = st.selectbox("Education Level", ["High School", "Bachelor", "Master", "PhD"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married"])

with col2:
    purpose = st.selectbox("Purpose of Visit", ["Tourism", "Study", "Work"])
    annual_income = st.number_input("Annual Income ($)", min_value=0)
    financial_proof = st.selectbox("Financial Proof Available", ["Yes", "No"])
    criminal_record = st.selectbox("Criminal Record", ["No", "Yes"])

# ===== BUTTON =====
if st.button("Check Eligibility"):

    with st.spinner("Analyzing your application... ⏳"):
        result, reason = retrieve_documents(age, country, visa_type)

    # ===== RESULT DISPLAY =====
    if result == "Eligible":
        st.balloons()
        st.success("🎉 Congratulations! You are Eligible!")
    else:
        st.error("❌ Sorry, You are Not Eligible")

    st.markdown(f"""
    <div class="result-box">
        <b>Reason:</b><br>{reason}
    </div>
    """, unsafe_allow_html=True)
