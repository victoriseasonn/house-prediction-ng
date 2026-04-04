import streamlit as st
from database import create_table, add_user, login_user
from scraper import get_live_prices

create_table()

st.set_page_config(page_title="Naija Property AI", page_icon="🏠")

# --- SIDEBAR ---
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

# --- LOGIN ---
if choice == "Login":
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        result = login_user(username, password)
        if result:
            st.session_state["user"] = username
            st.success(f"Welcome {username}")
        else:
            st.error("Invalid credentials")

# --- SIGNUP ---
elif choice == "Sign Up":
    st.title("📝 Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        add_user(new_user, new_pass)
        st.success("Account created successfully")

# --- DASHBOARD ---
if "user" in st.session_state:
    st.title(f"🏠 Welcome {st.session_state['user']}")

    states = [
        "Lagos","Abuja","Rivers","Oyo","Kano","Enugu",
        "Kaduna","Ogun","Imo","Anambra","Delta","Edo"
    ]

    state = st.selectbox("Select State", states)

    st.markdown("---")
    st.subheader("🤖 AI Price Prediction")

    house_type = st.selectbox("House Type", ["Flat","Bungalow","Duplex","Mansion"])
    bedrooms = st.slider("Bedrooms", 1, 10, 3)

    if st.button("Predict"):
        base = {
            "Flat": 10000000,
            "Bungalow": 15000000,
            "Duplex": 30000000,
            "Mansion": 80000000
        }

        state_factor = {
            "Lagos": 2.5,
            "Abuja": 2.2,
            "Rivers": 1.8,
            "Oyo": 1.5,
            "Kano": 1.3
        }

        price = base[house_type] * state_factor.get(state, 1.2)
        price += bedrooms * 2000000

        st.success(f"Estimated Price: ₦{price:,.0f}")

    st.markdown("---")
    st.subheader("🏘️ Market Listings")

    if st.button("Load Market Data"):
        df = get_live_prices(state)
        st.dataframe(df)
