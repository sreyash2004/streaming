import streamlit as st
from retrievalout import retrieve_documents

# ===== CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="wide")

# ===== SESSION =====
if "step" not in st.session_state:
    st.session_state.step = 1

countries = ["USA","Canada","UK","Germany","Australia","France","Italy","Spain","Netherlands","Sweden","Singapore","Japan","New Zealand","Ireland"]

# ===== CSS (RESPONSIVE & CENTERING FIX) =====
st.markdown("""
<style>
/* 1. CENTER THE MAIN WRAPPER */
.block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding-top: 2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* 2. FIX STREAMLIT'S INTERNAL ALIGNMENT */
[data-testid="stMarkdownContainer"] > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

/* 3. BACKGROUND & GLOBAL FONTS */
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
}

/* 4. MAIN TITLE */
.main-title {
    width: 100%;
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: clamp(24px, 5vw, 32px); /* Responsive font size */
    font-weight: bold;
    margin-bottom: 25px;
    box-sizing: border-box !important;
}

/* 5. BUTTON STYLING */
.stButton>button {
    width: 100%;
    height: 48px;
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* 6. THE RESULT CARD (FIXED FOR DESKTOP & MOBILE) */
.result-card {
    background: white;
    padding: 30px;
    border-radius: 14px;
    border-left: 8px solid #2563EB;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    width: 100% !important;
    margin: 30px auto !important;
    box-sizing: border-box !important; /* CRITICAL: Prevents width overflow */
    text-align: left;
}

.result-card h4 {
    color: #1e3a8a;
    margin-top: 20px;
    margin-bottom: 5px;
}

.result-card p {
    color: #334155;
    line-height: 1.6;
}

/* 7. SIDEBAR CUSTOMIZATION */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#2563EB,#38BDF8);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.title("⚠️ Important Notice")
st.sidebar.warning("AI-based visa checker\nNot official decision\nEmbassy has final authority")

# ===== HEADER =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI</div>', unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if st.session_state.step == 1:
    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name *")
    age = st.number_input("Age *", 1, 100, 25)
    marital = st.selectbox("Marital Status *", ["", "Single", "Married"])
    employment = st.selectbox("Employment *", ["", "Student", "Employed", "Unemployed"])
    education = st.selectbox("Education *", ["", "High School", "Bachelor", "Master", "PhD"])

    if st.button("Next ➡"):
        if not name or marital=="" or employment=="" or education=="":
            st.error("⚠️ Please fill all required fields")
        else:
            st.session_state.user = {"name": name, "age": age}
            st.session_state.step = 2

elif st.session_state.step == 2:
    st.subheader("🌍 Visa Details")
    country = st.selectbox("Destination Country *", [""] + countries)
    visa_type = st.selectbox("Visa Type *", ["", "Tourist","Student","Work"])
    travel = st.selectbox("Travel History *", ["","None","Few","Frequent"])
    finance = st.selectbox("Financial Proof *", ["","Yes","No"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"): st.session_state.step = 1
    with col2:
        if st.button("Next ➡"):
            if country=="" or visa_type=="" or travel=="" or finance=="":
                st.error("⚠️ Fill all fields")
            else:
                st.session_state.visa = {"country": country, "visa": visa_type}
                st.session_state.step = 3

elif st.session_state.step == 3:
    st.subheader("📊 Additional Info")
    ielts = st.number_input("IELTS Score *", 0.0, 9.0, 6.0, step=0.5)
    income = st.number_input("Annual Income ($) *", 0, 1000000, 30000)
    rejection = st.selectbox("Previous Visa Rejection *", ["","No","Yes"])
    criminal = st.selectbox("Criminal Record *", ["","No","Yes"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"): st.session_state.step = 2
    with col2:
        if st.button("Check Eligibility 🚀"):
            if rejection=="" or criminal=="":
                st.error("⚠️ Fill all fields")
            else:
                # API CALL
                result, reason = retrieve_documents(
                    st.session_state.user["age"],
                    st.session_state.visa["country"],
                    st.session_state.visa["visa"]
                )

                # CALCULATE SCORE
                score = 50
                if ielts >= 6.5: score += 15
                if income > 25000: score += 15
                if rejection == "No": score += 10
                if criminal == "No": score += 10
                score = min(score, 100)

                # DISPLAY RESULTS
                st.markdown("## 📊 Eligibility Result")
                if result == "Eligible":
                    st.success("🎉 You are Eligible!")
                else:
                    st.error("❌ Not Eligible")

                st.write(f"**Score:** {score}%")
                st.progress(score / 100)

                # CLEAN DATA FOR OUTPUT
                clean_reason = reason.replace("•", "").replace("**", "").strip()

                # FINAL OUTPUT CARD
                st.markdown(f"""
                <div class="result-card">
                    <h4>🔍 1. Visa Requirement Overview</h4>
                    <p>Requires official documentation and valid financial proof for {st.session_state.visa['country']}.</p>

                    <h4>📊 2. Eligibility Confidence Score</h4>
                    <p><b>{score}%</b> - Highly accurate based on current policy data.</p>

                    <h4>🧠 3. Detailed Analysis</h4>
                    <p>{clean_reason}</p>

                    <h4>📌 4. Decision Explanation</h4>
                    <p>This result is generated based on {st.session_state.visa['visa']} visa regulations and your personal profile strength.</p>
                </div>
                """, unsafe_allow_html=True)
