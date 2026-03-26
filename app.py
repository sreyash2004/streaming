import streamlit as st
from retrievalout import retrieve_documents

# ===== SESSION STATE =====
if "step" not in st.session_state:
    st.session_state.step = 1

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

# ===== CSS (IMPROVED UI) =====
st.markdown("""
<style>

/* ===== BACKGROUND (GRADIENT - NOT PLAIN) ===== */
.stApp {
    background: linear-gradient(135deg, #dbeafe, #e0f2fe, #f0f9ff);
}

/* ===== MAIN CARD ===== */
.block-container {
    background: #ffffff;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #cbd5f5;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

/* ===== TITLE ===== */
.main-title {
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    color: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 15px;
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: #0f172a !important;
}

/* ===== LABELS ===== */
label {
    color: #1e293b !important;
    font-weight: 600 !important;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #f8fafc !important;
    border-radius: 10px !important;
    border: 1px solid #93c5fd !important;
    color: #0f172a !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #3B82F6, #06B6D4);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 45px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: #f1f5f9;
    padding: 20px;
    border-left: 6px solid #2563EB;
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

</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.title("⚠️ Important Notice")

st.sidebar.warning("""
This is an AI-based visa eligibility system.

- Not an official visa authority  
- Results are predictive only  
- Final decision depends on embassy  
""")

st.sidebar.info("""
✔ Academic Project  
✔ AI + Rule-based System  
✔ For demonstration use only  
""")

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Smart Eligibility Checker</div>', unsafe_allow_html=True)

# =======================
# STEP 1
# =======================
if st.session_state.step == 1:

    st.subheader("👤 Personal Information")

    name = st.text_input("👤 Full Name *")
    age = st.number_input("🎂 Age *", min_value=0, max_value=100)
    nationality = st.text_input("🌎 Nationality *")

    marital = st.selectbox("💍 Marital Status *", ["", "Single", "Married"])
    education = st.selectbox("🎓 Education *", ["", "High School", "Bachelor", "Master", "PhD"])
    employment = st.selectbox("💼 Employment *", ["", "Student", "Employed", "Unemployed"])

    if st.button("Next ➡"):
        if not name or age == 0 or nationality == "" or marital == "" or education == "" or employment == "":
            st.error("⚠️ Fill all mandatory fields")
        else:
            st.session_state.user_data = {
                "name": name,
                "age": age,
                "nationality": nationality,
                "marital": marital,
                "education": education,
                "employment": employment
            }
            st.session_state.step = 2

# =======================
# STEP 2
# =======================
elif st.session_state.step == 2:

    st.subheader("🌍 Visa Details")

    country = st.selectbox("🌍 Destination Country *", ["", "USA", "Canada", "UK", "Germany", "Australia"])
    visa = st.selectbox("🛂 Visa Type *", ["", "Tourist", "Student", "Work"])
    purpose = st.selectbox("✈ Purpose *", ["", "Tourism", "Study", "Work"])

    travel = st.selectbox("🧳 Travel History *", ["", "None", "Few Countries", "Frequent Traveler"])
    finance = st.selectbox("💰 Financial Proof *", ["", "Yes", "No"])
    stay = st.selectbox("🏠 Accommodation *", ["", "Booked", "Not Booked"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 1

    with col2:
        if st.button("Next ➡"):
            if country == "" or visa == "" or purpose == "" or travel == "" or finance == "":
                st.error("⚠️ Fill all mandatory fields")
            else:
                st.session_state.visa_data = {
                    "country": country,
                    "visa": visa
                }
                st.session_state.step = 3

# =======================
# STEP 3
# =======================
elif st.session_state.step == 3:

    st.subheader("📊 Risk & Score Analysis")

    criminal = st.selectbox("⚖ Criminal Record *", ["", "No", "Yes"])
    income = st.number_input("💵 Annual Income ($) *", min_value=0)
    ielts = st.number_input("📘 IELTS Score *", min_value=0.0, max_value=9.0, step=0.5)
    rejection = st.selectbox("❌ Previous Visa Rejection *", ["", "No", "Yes"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 2

    with col2:
        if st.button("Check Eligibility 🚀"):

            if criminal == "" or income == 0 or ielts == 0 or rejection == "":
                st.error("⚠️ Fill all mandatory fields")
            else:
                result, reason = retrieve_documents(
                    st.session_state.user_data["age"],
                    st.session_state.visa_data["country"],
                    st.session_state.visa_data["visa"]
                )

                if result == "Eligible":
                    st.success("🎉 You are Eligible!")
                    st.balloons()
                else:
                    st.error("❌ Not Eligible")

                st.markdown(f"""
                <div class="result-box">
                {reason}
                </div>
                """, unsafe_allow_html=True)
