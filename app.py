import streamlit as st
from retrievalout import retrieve_documents

# ===== CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

# ===== CSS =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f0f9ff, #eef2ff);
}

.block-container {
    background: #ffffff;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.main-title {
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    color: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 20px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #3B82F6, #06B6D4);
    color: white;
    height: 50px;
    border-radius: 12px;
    font-weight: bold;
}

.result-box {
    background: #f1f5f9;
    padding: 20px;
    border-left: 6px solid #3B82F6;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Eligibility Checker</div>', unsafe_allow_html=True)

# =====================
# 👤 PERSONAL INFO
# =====================
st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)

name = st.text_input("Full Name")
age = st.number_input("Age", 0, 100)
nationality = st.text_input("Nationality")

col1, col2 = st.columns(2)

with col1:
    education = st.selectbox("Education Level", ["", "High School", "Bachelor", "Master", "PhD"])
    employment = st.selectbox("Employment Status", ["", "Student", "Employed", "Unemployed"])

with col2:
    criminal_record = st.selectbox("Criminal Record", ["", "No", "Yes"])
    previous_rejection = st.selectbox("Previous Visa Rejection", ["", "No", "Yes"])

# =====================
# 🌍 VISA INFO
# =====================
st.markdown('<div class="section-title">🌍 Visa Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Destination Country", ["", "USA", "Canada", "UK", "Australia", "Germany"])
    visa_type = st.selectbox("Visa Type", ["", "Tourist", "Student", "Work"])

with col2:
    purpose = st.selectbox("Purpose of Visit", ["", "Tourism", "Study", "Work"])
    ielts = st.selectbox("IELTS Exam Appeared", ["", "Yes", "No"])

# =====================
# 📊 ADDITIONAL INFO
# =====================
st.markdown('<div class="section-title">📊 Additional Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Annual Income ($)", 0)
    financial_proof = st.selectbox("Financial Proof Available", ["", "Yes", "No"])
    accommodation = st.selectbox("Accommodation Provided", ["", "Yes", "No"])

with col2:
    scholarship = st.selectbox("Any Scholarship Availed", ["", "Yes", "No"])
    sponsor = st.selectbox("Any Sponsor Taken", ["", "Yes", "No"])

# =====================
# 🚀 CHECK BUTTON
# =====================
if st.button("Check Eligibility 🚀"):

    # VALIDATION
    if age == 0 or country == "" or visa_type == "" or education == "":
        st.error("⚠️ Please fill all required fields")

    else:
        result, reason = retrieve_documents(age, country, visa_type)

        # =====================
        # 🔥 REAL DECISION LOGIC
        # =====================
        if criminal_record == "Yes":
            result = "Not Eligible"
            reason = "❌ Criminal record found. Visa will most likely be rejected."

        elif previous_rejection == "Yes":
            result = "Not Eligible"
            reason = "❌ Previous visa rejection detected."

        elif financial_proof == "No":
            result = "Not Eligible"
            reason = "❌ Financial proof is mandatory."

        # =====================
        # SCORE SYSTEM
        # =====================
        score = 50

        if ielts == "Yes": score += 10
        if income > 20000: score += 10
        if financial_proof == "Yes": score += 10
        if accommodation == "Yes": score += 10
        if sponsor == "Yes": score += 10

        score = min(score, 100)

        # =====================
        # RESULT DISPLAY
        # =====================
        st.markdown("## 📊 Eligibility Result")

        if result == "Eligible":
            st.success("🎉 You are Eligible!")
            st.balloons()
        else:
            st.error("❌ Not Eligible")

        st.write(f"**Score:** {score}%")
        st.progress(score/100)

        st.markdown(f"""
        <div class="result-box">
        {reason}
        </div>
        """, unsafe_allow_html=True)
