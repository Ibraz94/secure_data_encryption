# 🔒 Secure Data Encryption System

A Streamlit-based secure data storage and retrieval system. Users can store data with unique passkeys and decrypt it only with the correct passkey. The system operates entirely in memory.

## Features

- **Secure Data Storage**: Store sensitive data with encryption
- **Passkey Protection**: Access data only with the correct passkey
- **Security Lockout**: Multiple failed attempts result in a mandatory reauthorization
- **Time-based Lockout**: Additional security with timeout after failed attempts
- **User-friendly Interface**: Easy-to-use Streamlit UI

## Setup and Installation

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```
   streamlit run main.py
   ```

## How to Use

### Store Data
1. Navigate to "Store Data" in the sidebar
2. Enter a name for your data
3. Enter the data you want to encrypt
4. Create and confirm a passkey
5. Click "Encrypt & Save"

### Retrieve Data
1. Navigate to "Retrieve Data" in the sidebar
2. Select the data you want to retrieve
3. Enter the passkey
4. Click "Decrypt"

### Security Features
- After 3 failed passkey attempts, you'll be redirected to the login page
- Time-based lockout (2 minutes) after multiple failed attempts
- Master password for reauthorization: `admin123` (for demo purposes only)

## Security Notice

This is a demonstration application. In a production environment, additional security measures would be implemented:
- Stronger encryption methods
- Secure key management
- Proper user authentication

## Technical Details

- Uses Fernet symmetric encryption from the cryptography library
- SHA-256 hashing for passkeys
- Streamlit for the user interface
- Pure in-memory storage with no external database
