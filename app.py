import streamlit as st
import re
import random
import string
import requests
import hashlib

# ✅ Custom CSS for Dark Neon Theme
st.markdown("""
<style>
/* Background & Main Text */
.stApp {
    background-color: #121212;  /* Dark Gray, not pure black */
    color: #E0E0E0;  /* Light Gray */
}

/* Titles */
h1, h2, h3 {
    color: #00AEEF; /* Cybersecurity Blue */
}

/* Paragraphs & Labels */
p, label {
    font-size: 18px;
    color: #E0E0E0;
}

/* Buttons */
div.stButton > button {
    background-color: #1E88E5; /* Professional Blue */
    color: white !important;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    box-shadow: 0px 0px 8px #1E88E5;
}

div.stButton > button:hover {
    background-color: #1565C0;
    box-shadow: 0px 0px 12px #1E88E5;
}

/* Input Fields */
input {
    background-color: #222;
    color: black !important;
    border: 1px solid #444;
    padding: 8px;
    border-radius: 5px;
}

</style>

""", unsafe_allow_html=True)

# 🔷 Add a Main Title
st.markdown('<h1 class="title">🔐 Random Strong Password Generator & Strength Meter</h1>', unsafe_allow_html=True)

# 🔷 Introduction
st.write("""
Welcome! This tool helps you **generate a strong password** or **check the strength** of your own password. 
A strong password keeps your accounts **safe from hackers**! 🚀
""")

# ✅ Function to Check If Password is Pwned
def is_password_pwned(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    first5, rest = sha1_hash[:5], sha1_hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    response = requests.get(url)
    
    if response.status_code == 200:
        hashes = (line.split(":") for line in response.text.splitlines())
        if any(h == rest for h, _ in hashes):
            return True  # Password is in breach database
    return False  # Safe password

def check_password_strength(password):
    score = 0
    feedback = []

    # ✅ Check if password is pwned
    if is_password_pwned(password):
        st.error("⚠️ This password has been **leaked in data breaches**! Choose a **different one**! 🛑")
        return

    # ✅ Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # ✅ Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # ✅ Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # ✅ Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # 🔹 Strength Rating
    if score == 4:
        st.success("✅ Strong Password! 🔥")
        bar_color = "green"
    elif score == 3 or score == 2:
        st.warning("⚠️ Moderate Password - Consider adding more security features.")
        bar_color = "yellow"
    else:
        st.error("❌ Weak Password - Improve it using the suggestions below.")
        bar_color = "red"

    # ✅ Add Progress Bar with Color Change
    st.write("Strength meter")
    st.write(f"Score: {score}/4")

    # Custom CSS for progress bar color
    st.markdown(
        f"""
        <style>
        .stProgress > div > div > div > div {{
            background-color: {bar_color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.progress(score / 4)

    # Show feedback messages
    for message in feedback:
        st.write(message)

with st.expander("📜 First check the Password Strength Rules"):
    st.write("""
    - ✅ **At least 8 characters** (longer is better)
    - ✅ **Mix of uppercase & lowercase letters** (Aa-Zz)
    - ✅ **Include numbers** (0-9)
    - ✅ **Use special characters** (!@#$%^&*)
    - ❌ **Avoid common passwords** (e.g., "password123")
    """)

# 🔷 Section: Random Password Generator
st.header("🎲 Generate a Secure Random Password")
st.write("""
Want a strong password that’s **hard to guess**?  
Select a length and click the **Generate Password** button!  
""")

def generate_password(length=12):
    # ✅ Check if password length is valid:
    if length < 8:
        return "⚠️ Password should be at least 8 characters long!"
    
    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")
    
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining_length = length - 4

    random_chars = ''.join(random.choice(all_characters) for _ in range(remaining_length))
    
    # ✅ Combine all characters and shuffle them
    password = list(uppercase + lowercase + digit + special + random_chars)
    random.shuffle(password)

    return ''.join(password)

# Let user select password length
length = st.slider("Select password length:", min_value=8, max_value=32, value=12)

if st.button("Generate password"):
    new_password = generate_password(length)
    st.success(f"Your generated password: {new_password}")
    
    # ✅ Copy to Clipboard Button
    st.write("Copy to clipboard")
    st.code(new_password, language="")

# 🔷 Section: Check Your Own Password Strength
st.header("🛡 Check Your Own Password Strength")
st.write("""
Already have a password? Type it below to see if it's **strong enough**!  
We'll check its **length, mix of characters, and security level**.  
""")

# ✅ Get user input
password = st.text_input("Enter your password:", type="password")
check_strength = st.button("🔍 Check Strength")

if check_strength:
    if password:
        check_password_strength(password)
    else:
        st.warning("⚠️ Please enter a password first!")
