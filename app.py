import streamlit as st
from retrievalout import retrieve_documents

# ===== CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

# ===== CSS (FIXED ALIGNMENT) =====
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#eef2ff,#f8fafc);
}

.block-container {
    max-width: 850px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

/* CENTER FIX */
div[data-testid="stMarkdownContainer"] p {
    text-align: left !important;
}

/* TITLE */
.title-box {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #2563EB;
    margin-bottom: 20px;
}

/* SECTION */
.section {
    font-size: 20px;
    font-weight: 600;
    margin-top: 25px;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    height: 50px;
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

/* RESULT BOX */
.result-box {
    background: #f1f5f9;
    padding: 18px;
    border-radius: 10px;
    border-left: 5px solid #2563EB;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="title-box">🌍 SwiftVisa AI - Eligibility Checker</div>', unsafe_allow_html=True)

# ======================
# 👤 PERSONAL INFO
# ======================
st.markdown('<div class="section">👤 Personal Information</div>', unsafe_allow_html=True)

name = st.text_input("Full Name")
age = st.number_input("Age", 0, 100)

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox("Destination Country", ["", "USA", "Canada", "UK", "Australia", "Germany"])
    visa_type = st.selectbox("Visa Type", ["", "Tourist", "Student", "Work"])

with col2:
    passport = st.selectbox("Valid Passport Available", ["", "Yes", "No"])
    criminal_record = st.selectbox("Criminal Record", ["", "No", "Yes"])

# ======================
# 📊 CORE VISA CHECK
# ======================
st.markdown('<div class="section">📊 Core Visa Factors</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    financial_proof = st.selectbox("Financial Proof Available", ["", "Yes", "No"])

with col2:
    previous_rejection = st.selectbox("Previous Visa Rejection", ["", "No", "Yes"])

# ======================
# 🟡 OPTIONAL INFO
# ======================
st.markdown('<div class="section">🟡 Optional (Improves Chances)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    ielts = st.selectbox("Have you appeared for IELTS?", ["", "Yes", "No"])
    income = st.number_input("Annual Income ($)", 0)

with col2:
    accommodation = st.selectbox("Accommodation Arranged", ["", "Yes", "No"])
    sponsor = st.selectbox("Sponsor Available", ["", "Yes", "No"])

# IELTS conditional
ielts_score = None
if ielts == "Yes":
    ielts_score = st.number_input("IELTS Score (0 - 9)", 0.0, 9.0)

# ======================
# 🚀 BUTTON
# ======================
if st.button("Check Eligibility 🚀"):

    # ===== VALIDATION =====
    if (
        name.strip() == "" or
        age == 0 or
        country == "" or
        visa_type == "" or
        passport == "" or
        criminal_record == "" or
        financial_proof == "" or
        previous_rejection == ""
    ):
        st.error("⚠️ Please fill all mandatory fields")

    else:
        result, reason = retrieve_documents(age, country, visa_type)

        improvements = []
        steps = []

        # ======================
        # 🔴 STRICT RULES
        # ======================
        if passport == "No":
            result = "Not Eligible"
            reason = "❌ Valid passport is required."

        elif criminal_record == "Yes":
            result = "Not Eligible"
            reason = "❌ Criminal record found."

        elif previous_rejection == "Yes":
            result = "Not Eligible"
            reason = "❌ Previous visa rejection detected."

        elif financial_proof == "No":
            result = "Not Eligible"
            reason = "❌ Financial proof is mandatory."

        # ======================
        # 🧠 SCORE SYSTEM
        # ======================
        score = 50

        if ielts == "Yes":
            if ielts_score and ielts_score >= 6:
                score += 10
            else:
                improvements.append("Improve IELTS score")
                steps.append("Try to achieve at least 6+ band")

        else:
            improvements.append("Consider taking IELTS")
            steps.append("IELTS improves approval chances")

        if income > 20000:
            score += 10
        else:
            improvements.append("Increase income stability")
            steps.append("Show stable income or job proof")

        if accommodation == "Yes":
            score += 10
        else:
            improvements.append("Arrange accommodation")
            steps.append("Provide hotel booking or invitation letter")

        if sponsor == "Yes":
            score += 10

        score = min(score, 100)

        # ======================
        # 📊 OUTPUT
        # ======================
        st.markdown("## 📊 Result")

        if result == "Eligible":
            st.success("🎉 You are Eligible!")
            st.balloons()

        else:
            st.error("❌ Not Eligible")

            st.markdown("### 🔧 Improvements Needed")
            for i in improvements:
                st.write(f"• {i}")

            st.markdown("### 🚀 Steps to Improve")
            for s in steps:
                st.write(f"• {s}")

        st.write(f"**Score:** {score}%")
        st.progress(score / 100)

        st.markdown(f"""
        <div class="result-box">
        {reason}
        </div>
        """, unsafe_allow_html=True)
