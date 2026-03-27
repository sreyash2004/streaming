import streamlit as st
from retrievalout import retrieve_documents

# ===== CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="wide")

# ===== SESSION =====
if "step" not in st.session_state:
    st.session_state.step = 1

countries = [
    "USA","Canada","UK","Germany","Australia",
    "France","Italy","Spain","Netherlands",
    "Sweden","Singapore","Japan","New Zealand","Ireland"
]

# ===== CSS (STRICT CENTERING FIX) =====
st.markdown("""
<style>

/* 1. FORCE THE MAIN CONTAINER TO BE CENTERED */
.block-container {
    max-width: 850px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* 2. FIX THE 'TILT' - FORCES THE MARKDOWN ELEMENT TO BE FULL WIDTH */
[data-testid="stMarkdownContainer"] > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* 3. BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
}

/* 4. RESULT CARD - ADDING BOX-SIZING IS KEY */
.result-card {
    background: white;
    padding: 30px;
    border-radius: 14px;
    border-left: 8px solid #2563EB;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    
    /* This ensures the card stays centered within the 850px lane */
    width: 100%; 
    max-width: 800px;
    margin: 20px auto !important;
    
    /* Prevents internal content from pushing the card's width out */
    box-sizing: border-box; 
    text-align: left;
}

/* 5. TITLE ALIGNMENT */
.main-title {
    width: 100%;
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color:white;
    padding:20px;
    border-radius:12px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
    margin-bottom:25px;
    box-sizing: border-box;
}

/* 6. SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#2563EB,#38BDF8);
}
section[data-testid="stSidebar"] * {
    color:white !important;
}

</style>
""", unsafe_allow_html=True)
# ===== SIDEBAR =====
st.sidebar.title("⚠️ Important Notice")
st.sidebar.warning("AI-based visa checker\nNot official decision\nEmbassy has final authority")

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI</div>', unsafe_allow_html=True)

# ======================
# STEP 1
# ======================
if st.session_state.step == 1:

    st.subheader("👤 Personal Information")

    name = st.text_input("Full Name *")
    age = st.number_input("Age *", 0, 100)

    marital = st.selectbox("Marital Status *", ["", "Single", "Married"])
    employment = st.selectbox("Employment *", ["", "Student", "Employed", "Unemployed"])
    education = st.selectbox("Education *", ["", "High School", "Bachelor", "Master", "PhD"])

    if st.button("Next ➡"):
        if not name or age == 0 or marital=="" or employment=="" or education=="":
            st.error("⚠️ Fill all fields")
        else:
            st.session_state.user = {"age": age}
            st.session_state.step = 2

# ======================
# STEP 2
# ======================
elif st.session_state.step == 2:

    st.subheader("🌍 Visa Details")

    country = st.selectbox("Destination Country *", [""]+countries)
    visa = st.selectbox("Visa Type *", ["", "Tourist","Student","Work"])

    travel = st.selectbox("Travel History *", ["","None","Few","Frequent"])
    finance = st.selectbox("Financial Proof *", ["","Yes","No"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 1

    with col2:
        if st.button("Next ➡"):
            if country=="" or visa=="" or travel=="" or finance=="":
                st.error("⚠️ Fill all fields")
            else:
                st.session_state.visa = {"country":country,"visa":visa}
                st.session_state.step = 3

# ======================
# STEP 3
# ======================
elif st.session_state.step == 3:

    st.subheader("📊 Additional Info")

    ielts = st.number_input("IELTS Score *",0.0,9.0,step=0.5)
    income = st.number_input("Annual Income ($) *",0)

    rejection = st.selectbox("Previous Visa Rejection *", ["","No","Yes"])
    criminal = st.selectbox("Criminal Record *", ["","No","Yes"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 2

    with col2:
        if st.button("Check Eligibility 🚀"):

            if ielts==0 or income==0 or rejection=="" or criminal=="":
                st.error("⚠️ Fill all fields")
            else:
                result, reason = retrieve_documents(
                    st.session_state.user["age"],
                    st.session_state.visa["country"],
                    st.session_state.visa["visa"]
                )

                # SCORE
                score = 50
                if ielts >= 6: score += 15
                if income > 20000: score += 15
                if rejection == "No": score += 10
                if criminal == "No": score += 10
                score = min(score, 100)

                # RESULT
                st.markdown("## 📊 Eligibility Result")

                if result == "Eligible":
                    st.success("🎉 You are Eligible!")
                else:
                    st.error("❌ Not Eligible")

                st.write(f"**Score:** {score}%")
                st.progress(score / 100)

                clean_reason = reason.replace("•", "").replace("**", "").strip()

                # FINAL CARD
                st.markdown(f"""
                <div class="result-card">

                <h4>🔍 1. Visa Requirement Overview</h4>
                <p>Requires I-20 form and financial proof.</p>

                <h4>📊 2. Eligibility Confidence Score</h4>
                <p><b>{score}%</b></p>

                <h4>🧠 3. Detailed Analysis</h4>
                <p>{clean_reason}</p>

                <h4>📌 4. Decision Explanation</h4>
                <p>Based on eligibility rules and profile strength.</p>

                </div>
                """, unsafe_allow_html=True)
