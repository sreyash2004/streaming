import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

# ===== CUSTOM CSS =====
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(rgba(240,245,255,0.9), rgba(240,245,255,0.9)),
    url("https://images.unsplash.com/photo-1502920917128-1aa500764cbd");
    background-size: cover;
    background-attachment: fixed;
}

/* Title */
.main-title {
    background: linear-gradient(90deg, #4F46E5, #06B6D4);
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}

/* Card container */
.block-container {
    background: rgba(255,255,255,0.92);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #06B6D4, #3B82F6);
    color: white;
    font-weight: bold;
    height: 50px;
    border-radius: 12px;
}

/* Result box */
.result-box {
    background: #ffffff;
    padding: 20px;
    border-left: 6px solid #3B82F6;
    border-radius: 10px;
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
