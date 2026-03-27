import streamlit as st
from retrievalout import retrieve_documents

# ===== SESSION =====
if "step" not in st.session_state:
    st.session_state.step = 1

# ===== CONFIG =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="wide")

countries = [
    "USA","Canada","UK","Germany","Australia",
    "France","Italy","Spain","Netherlands",
    "Sweden","Singapore","Japan","New Zealand","Ireland"
]

# ===== CSS =====
st.markdown("""
<style>

/* CENTER */
.block-container {
    max-width: 850px;
    margin: auto;
    padding: 2rem;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
}

/* TITLE */
.main-title {
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color:white;
    padding:16px;
    border-radius:12px;
    text-align:center;
    font-size:30px;
    font-weight:bold;
}

/* INPUTS */
input, .stSelectbox div {
    background:#ffffff !important;
    color:#0f172a !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#2563EB,#06B6D4);
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:42px;
}

/* RESULT BOX */
.result-box {
    background: linear-gradient(135deg,#ffffff,#e0f2fe);
    padding:25px;
    border-radius:15px;
    border-left:8px solid #2563EB;
    box-shadow:0 8px 20px rgba(0,0,0,0.08);
    color:#0f172a;
    font-size:16px;
    line-height:1.6;
}

/* SIDEBAR */
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
st.sidebar.warning("""
AI-based visa checker  
Not official decision  
Embassy has final authority
""")

st.sidebar.info("""
✔ Academic Project  
✔ AI + Rule-based  
✔ Demo Purpose  
""")

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

    col1,col2 = st.columns(2)

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

    col1,col2 = st.columns(2)

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

                # ===== SCORE LOGIC =====
                score = 50

                if ielts >= 6: score += 15
                if income > 20000: score += 15
                if rejection == "No": score += 10
                if criminal == "No": score += 10

                score = min(score, 100)

                # ===== RESULT =====
                if result=="Eligible":
                    st.success("🎉 You are Eligible!")
                    st.balloons()
                else:
                    st.error("❌ Not Eligible")

                # ===== SCORE BAR =====
                st.progress(score / 100)
                st.write(f"### 📊 Eligibility Score: {score}%")

                # ===== EXPLANATION =====
                st.markdown(f"""
                <div class="result-box">
                {reason}
                </div>
                """, unsafe_allow_html=True)
