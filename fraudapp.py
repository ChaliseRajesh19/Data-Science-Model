import streamlit as st
import pickle
import pandas as pd
import cloudpickle

# Load the trained model
with open('fraud_detection_model.pkl', 'rb') as f:
    pipe = cloudpickle.load(f)

st.title("🔐 Fraud Detection Prediction App")

# Input fields
acc_days = st.number_input("🗓️ Account Activation Days", min_value=0, max_value=365, value=80)
failed_logins = st.number_input("❌ Failed Login Attempts", min_value=0, max_value=20, value=1)
transaction_amount = st.number_input("💰 Transaction Amount", min_value=0.0, max_value=1_000_000.0, value=320.50)
items_quantity = st.number_input("📦 Items Quantity", min_value=1, max_value=100, value=3)
pages_viewed = st.number_input("📄 Pages Viewed", min_value=0, max_value=100, value=12)
purchase_frequency_user = st.number_input("🔁 User Purchase Frequency", min_value=0.0, max_value=100.0, value=2.5)

is_vpn_or_proxy = st.selectbox("🕵️ Using VPN or Proxy?", ["Yes", "No"])
is_card_blacklisted = st.selectbox("🚫 Is Card Blacklisted?", ["Yes", "No"])
is_multiple_cards_used = st.selectbox("💳 Multiple Cards Used?", ["Yes", "No"])
device_change = st.selectbox("🔄 Device Change During Session?", ["Yes", "No"])

# New: Category dropdown
category = st.selectbox("🛍️ Transaction Category", ["Beauty", "Electronics", "Fashion", "Groceries", "Home Appliances"])

# Convert to binary flags
vpn_flag = 1 if is_vpn_or_proxy == "Yes" else 0
blacklist_flag = 1 if is_card_blacklisted == "Yes" else 0
multi_card_flag = 1 if is_multiple_cards_used == "Yes" else 0
device_change_flag = 1 if device_change == "Yes" else 0

# When user clicks predict
if st.button("🔎 Predict Fraudulent Transaction"):
    input_dict = {
        'acc_days': acc_days,
        'transaction_amount': transaction_amount,
        'purchase_frequency_user': purchase_frequency_user,
        'pages_viewed': pages_viewed,
        'items_quantity': items_quantity,
        'failed_logins': failed_logins,
        'is_card_blacklisted': blacklist_flag,
        'is_vpn_or_proxy': vpn_flag,
        'device_change_during_session': device_change_flag,
        'is_multiple_cards_used': multi_card_flag,
        'category_Beauty': 0,
        'category_Electronics': 0,
        'category_Fashion': 0,
        'category_Groceries': 0,
        'category_Home Appliances': 0
    }

    # Set selected category to 1
    input_dict[f'category_{category}'] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Predict
    prediction = pipe.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠️ Fraudulent Transaction Detected!")
    else:
        st.success("✅ Transaction is Legitimate.")
