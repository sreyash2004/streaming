import streamlit as st
from retrievalout import retrieve_documents

# ===== PAGE CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="centered")

# ===== CUSTOM UI =====
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.82), rgba(255,255,255,0.82)),
    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Hide default */
header {visibility: hidden;}
footer {visibility: hidden;}

/* ===== TITLE ===== */
.main-title {
    background: linear-gradient(90deg, #1E3A8A, #2563EB);
    color: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    animation: fadeInDown 1s ease-in-out;
}

/* ===== CONTAINER ===== */
.block-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.15);
}

/* ===== LABELS ===== */
label {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 12px !important;
    border: 1px solid #cbd5f5 !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #2563EB, #1E40AF);
    color: white;
    font-weight: bold;
    border-radius: 14px;
    height: 50px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 20px rgba(37,99,235,0.4);
}

/* ===== RESULT BOX ===== */
.result-box {
    background: #ffffff;
    color: #111827;
    padding: 20px;
    border-radius: 14px;
    border-left: 6px solid #2563EB;
    font-size: 16px;
    line-height: 1.6;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* ===== ANIMATION ===== */
@keyframes fadeInDown {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Eligibility Checker</div>', unsafe_allow_html=True)

st.markdown("## 📝 Applicant Details")

# ===== FORM =====
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=0, max_value=100)
country = st.selectbox("Select Country", [
    "USA", "Canada", "UK", "Australia", "Germany",
    "France", "Japan", "UAE", "Singapore", "India"
])
visa_type = st.selectbox("Visa Type", ["Tourist", "Student", "Work"])

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
