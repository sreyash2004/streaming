import streamlit as st
from retrievalout import retrieve_documents

# ===== SESSION STATE =====
if "step" not in st.session_state:
    st.session_state.step = 1

# ===== PAGE CONFIG (IMPORTANT FIX) =====
st.set_page_config(page_title="SwiftVisa AI", page_icon="🌍", layout="wide")

# ===== COUNTRIES =====
countries = [
    "USA", "Canada", "UK", "Germany", "Australia",
    "France", "Italy", "Spain", "Netherlands",
    "Sweden", "Singapore", "Japan", "New Zealand", "Ireland"
]

# ===== CSS (FIXED CENTER ISSUE) =====
st.markdown("""
<style>

/* CENTER CONTENT */
.block-container {
    max-width: 900px;
    margin: auto;
    padding: 2rem;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #dbeafe, #e0f2fe, #f0f9ff);
}

/* TITLE */
.main-title {
    background: linear-gradient(90deg, #2563EB, #06B6D4);
    color: white;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 15px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #3B82F6, #06B6D4);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 42px;
}

/* RESULT BOX */
.result-box {
    background: #f1f5f9;
    padding: 20px;
    border-left: 6px solid #2563EB;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 SwiftVisa AI - Smart Eligibility Checker</div>', unsafe_allow_html=True)

# =======================
# STEP 1
# =======================
if st.session_state.step == 1:

    st.subheader("👤 Personal Information")

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=100)
    education = st.selectbox("Education *", ["", "High School", "Bachelor", "Master", "PhD"])

    if st.button("Next ➡"):
        if education == "" or age == 0:
            st.error("Fill required fields")
        else:
            st.session_state.user_data = {"age": age}
            st.session_state.step = 2


# =======================
# STEP 2
# =======================
elif st.session_state.step == 2:

    st.subheader("🌍 Visa Details")

    country = st.selectbox("Destination Country *", [""] + countries)
    visa = st.selectbox("Visa Type *", ["", "Tourist", "Student", "Work"])

    finance = st.selectbox("Financial Proof *", ["", "Yes", "No"])
    criminal = st.selectbox("Criminal Record *", ["", "No", "Yes"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 1

    with col2:
        if st.button("Next ➡"):
            if country == "" or visa == "" or finance == "" or criminal == "":
                st.error("Fill required fields")
            else:
                st.session_state.visa_data = {
                    "country": country,
                    "visa": visa,
                    "criminal": criminal
                }
                st.session_state.step = 3


# =======================
# STEP 3 (IELTS LOGIC)
# =======================
elif st.session_state.step == 3:

    st.subheader("📊 Additional Details")

    ielts_taken = st.selectbox("Did you attend IELTS?", ["", "Yes", "No"])

    ielts_score = 0

    if ielts_taken == "Yes":
        ielts_score = st.number_input("IELTS Score", 0.0, 9.0, step=0.5)

    rejection = st.selectbox("Previous Visa Rejection *", ["", "No", "Yes"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = 2

    with col2:
        if st.button("Check Eligibility 🚀"):

            if ielts_taken == "" or rejection == "":
                st.error("Fill required fields")
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
