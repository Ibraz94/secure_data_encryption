import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import os
import time
from datetime import datetime, timedelta


if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'last_failed_time' not in st.session_state:
    st.session_state.last_failed_time = None
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# Function to hash passkey using SHA-256
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    try:
        hashed_passkey = hash_passkey(passkey)
        
        for key, value in st.session_state.stored_data.items():
            if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
                st.session_state.failed_attempts = 0
                return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
        
        st.session_state.failed_attempts += 1
        st.session_state.last_failed_time = datetime.now()
        return None
    except Exception:
        st.session_state.failed_attempts += 1
        st.session_state.last_failed_time = datetime.now()
        return None

# Check for lockout
def is_locked_out():
    if st.session_state.last_failed_time is not None:
        time_since_last_failure = datetime.now() - st.session_state.last_failed_time
        if st.session_state.failed_attempts >= 3 and time_since_last_failure < timedelta(minutes=2):
            return True
    return False


st.title("🔒 Secure Data Encryption System")


menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)


if st.session_state.failed_attempts > 0:
    st.sidebar.warning(f"⚠️ Failed attempts: {st.session_state.failed_attempts}/3")


if is_locked_out() and choice != "Login":
    st.error("🔒 Too many failed attempts! Please reauthorize.")
    choice = "Login"

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    
    st.info("""
    **How it works:**
    1. Store your data with a unique passkey
    2. Retrieve your data by providing the correct passkey
    3. After 3 failed attempts, you'll need to reauthorize
    """)

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    
    data_name = st.text_input("Data Name (for reference):")
    user_data = st.text_area("Enter Data to Encrypt:")
    passkey = st.text_input("Create Passkey:", type="password")
    confirm_passkey = st.text_input("Confirm Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if not data_name:
            st.error("⚠️ Please provide a name for your data!")
        elif not user_data:
            st.error("⚠️ Please enter some data to encrypt!")
        elif not passkey:
            st.error("⚠️ Please create a passkey!")
        elif passkey != confirm_passkey:
            st.error("⚠️ Passkeys do not match!")
        else:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            
            st.session_state.stored_data[data_name] = {
                "encrypted_text": encrypted_text, 
                "passkey": hashed_passkey,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.success("✅ Data stored securely!")
            st.info(f"Your data is stored with the name: **{data_name}**")

elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    
    if not st.session_state.stored_data:
        st.warning("No data has been stored yet. Please store some data first.")
    else:
        data_names = list(st.session_state.stored_data.keys())
        selected_data = st.selectbox("Select data to retrieve:", data_names)
        
        passkey = st.text_input("Enter Passkey:", type="password")

        if st.button("Decrypt"):
            if passkey:
                encrypted_text = st.session_state.stored_data[selected_data]["encrypted_text"]
                decrypted_text = decrypt_data(encrypted_text, passkey)

                if decrypted_text:
                    st.success("✅ Data decrypted successfully!")
                    st.code(decrypted_text)
                    st.button("Copy to Clipboard", 
                             on_click=lambda: st.write("Text copied to clipboard!"))
                else:
                    remaining = 3 - st.session_state.failed_attempts
                    if remaining > 0:
                        st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
                    else:
                        st.error("❌ Incorrect passkey! No attempts remaining.")
                        st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                        st.session_state.current_page = "Login"
                        st.experimental_rerun()
            else:
                st.error("⚠️ Please enter your passkey!")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    master_password = "admin123"  
    
    if st.session_state.last_failed_time is not None:
        time_since_last_failure = datetime.now() - st.session_state.last_failed_time
        if time_since_last_failure < timedelta(minutes=2):
            lockout_remaining = int((timedelta(minutes=2) - time_since_last_failure).total_seconds())
            if lockout_remaining > 0:
                st.warning(f"🔒 Account is locked for {lockout_remaining} more seconds.")
    
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == master_password:
            st.session_state.failed_attempts = 0
            st.session_state.last_failed_time = None
            st.success("✅ Reauthorized successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")

st.sidebar.subheader("System Status")
st.sidebar.info(f"Items in storage: {len(st.session_state.stored_data)}")
if st.session_state.failed_attempts >= 3:
    st.sidebar.error("🔒 Security lockout active")
elif st.session_state.failed_attempts > 0:
    st.sidebar.warning(f"⚠️ Failed attempts: {st.session_state.failed_attempts}/3")
else:
    st.sidebar.success("✅ System secure")

st.markdown("---") 
st.markdown(
        """
        <div style="text-align: center; color: #888888; padding: 20px;">
            <p>Secure Data Encryption System | Version 1.0</p>
            <p style='font-size: 0.8em;'>© 2025 All rights reserved</p>
            <p style='font-size: 0.8em;'>Created by Ibraz Ur Rehman</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
