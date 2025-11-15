# 💳 BNPL Risk Scoring System

A lightweight **Streamlit web application** that evaluates a user’s BNPL (Buy Now Pay Later) eligibility using a trained machine learning model. The system predicts the **risk score**, classifies the user, and assigns a **BNPL spending limit** based on demographic, financial, and behavioral factors.

---

## 🚀 Features

- 📈 Machine Learning–powered risk scoring  
- 🧮 Automatic BNPL limit calculation  
- 📝 Clean, user-friendly Streamlit interface  
- 🎓 Student-specific feature support  
- 🔐 Background behavioral data generated automatically  
- ⚡ Fast and intuitive workflow  

---

## 📂 Project Structure

├── app.py # Streamlit application

├── bnpl_model.pkl # Trained ML model (not included)

├── requirements.txt # Python dependencies

└── README.md # Project documentation

---

## 🏗️ How It Works

### 1️⃣ User enters:
- Age, gender  
- Monthly income and rent  
- Education level  
- Scholarship amount  
- Student / freelancer status  

### 2️⃣ App generates hidden features:
- Monthly expenses  
- Transaction behavior  
- Credit history metrics  
- Student GPA & certification count  

### 3️⃣ ML model outputs:
- **Risk Score** (0.00 – 1.00)

### 4️⃣ System assigns decision:

| Risk Score | Decision | Limit |
|------------|----------|--------|
| < 0.15 | Approve | High Limit |
| < 0.35 | Approve (Low Limit) | Low Limit |
| < 0.60 | Manual Review | — |
| ≥ 0.60 | Reject | 0 AZN |

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
