import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model
model = joblib.load("D:/hakaton/bnpl_model.pkl")

# ----- Risk Classification -----
def classify_user(risk_score):
    if risk_score < 0.15:
        return "Approve"
    elif risk_score < 0.35:
        return "Approve (Low Limit)"
    elif risk_score < 0.60:
        return "Manual Review"
    else:
        return "Reject"

# ----- Limit Calculation -----
def calculate_limit(risk_score, base_limit=150):
    return max(0, round(base_limit * (1 - risk_score), 2))

# ---------------- UI ----------------
st.set_page_config(page_title="BNPL Risk Engine", page_icon="💳", layout="centered")

st.markdown("""
    <h1 style='text-align:center;'>💳 BNPL Risk Scoring System</h1>
    <p style='text-align:center; color:gray;'>Enter basic details — the system estimates the risk and assigns a BNPL limit.</p>
""", unsafe_allow_html=True)

st.subheader("👤 User Basic Information")

col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input("First Name", "")
    age = st.number_input("Age", 18, 75, 25)
    gender = st.selectbox("Gender", ["male", "female", "other"])

with col2:
    last_name = st.text_input("Last Name", "")
    monthly_income = st.number_input("Monthly Income (AZN)", 0, 10000, 1200)
    monthly_rent = st.number_input("Monthly Rent (AZN)", 0, 4000, 800)

st.subheader("🎓 Additional Profile")

col3, col4 = st.columns(2)

with col3:
    is_student = st.selectbox("Are you a Student?", ["no", "yes"])
    education_level = st.selectbox("Education Level", ["High School", "Bachelor", "Master", "PhD"])

with col4:
    is_freelancer = st.selectbox("Are you a Freelancer?", ["no", "yes"])
    scholarship_amount = st.number_input("Scholarship Amount (AZN)", 0, 3000, 0)

# -------------------- HIDDEN BACKGROUND FIELDS --------------------

food_expenses = np.random.uniform(80, 300)
utilities_expenses = np.random.uniform(60, 150)
entertainment_expenses = np.random.uniform(20, 200)

monthly_transactions_amount = np.random.uniform(300, 2000)
num_transactions = np.random.randint(5, 60)

credit_history_num_loans = np.random.randint(0, 5)
credit_history_num_defaults = np.random.randint(0, 2)
credit_history_max_delay_days = np.random.randint(0, 40)

student_gpa = np.random.uniform(2.0, 4.0) if is_student == "yes" else 0
student_certifications_count = np.random.randint(0, 5) if is_student == "yes" else 0

# ---------------- Prepare input for model ----------------
input_data = pd.DataFrame([{
    "age": age,
    "gender": gender,
    "education_level": education_level,
    "monthly_income": monthly_income,
    "monthly_rent": monthly_rent,
    "food_expenses": float(food_expenses),
    "utilities_expenses": float(utilities_expenses),
    "entertainment_expenses": float(entertainment_expenses),
    "monthly_transactions_amount": float(monthly_transactions_amount),
    "num_transactions": int(num_transactions),
    "credit_history_num_loans": int(credit_history_num_loans),
    "credit_history_num_defaults": int(credit_history_num_defaults),
    "credit_history_max_delay_days": int(credit_history_max_delay_days),
    "scholarship_amount": scholarship_amount,
    "student_gpa": float(student_gpa),
    "student_certifications_count": int(student_certifications_count),
    "is_freelancer": 1 if is_freelancer == "yes" else 0
}])

# ---------------- RESULTS ----------------
st.subheader("📊 BNPL Risk Assessment")

if st.button("Calculate Risk Score"):
    risk_score = float(model.predict_proba(input_data)[0, 1])
    decision = classify_user(risk_score)

    # Limit logic
    if decision == "Approve":
        limit = calculate_limit(risk_score, 200)
    elif decision == "Approve (Low Limit)":
        limit = calculate_limit(risk_score, 100)
    else:
        limit = 0  # Reject or Manual Review

    # Display Results
    if decision == "Approve":
        st.success(f"""
            **Risk Score:** `{risk_score:.3f}`  
            **Decision:** `{decision}`  
            **BNPL Limit:** `{limit}AZN`
        """)
    elif decision == "Approve (Low Limit)":
        st.info(f"""
            **Risk Score:** `{risk_score:.3f}`  
            **Decision:** `{decision}`  
            **BNPL Limit:** `{limit}AZN`
        """)
    elif decision == "Manual Review":
        st.warning(f"""
            **Risk Score:** `{risk_score:.3f}`  
            **Decision:** `Manual Review Required`  
            **BNPL Limit:** *Not assigned*
        """)
    else:
        st.error(f"""
            **Risk Score:** `{risk_score:.3f}`  
            **Decision:** `Rejected`  
            **BNPL Limit:** `0 AZN`
        """)

    # Progress bar (fix float32 issue)
    st.progress(int(risk_score * 100))
    