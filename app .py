import streamlit as st
import pandas as pd
from scraper import get_live_prices

# --- PAGE SETUP ---
st.set_page_config(page_title="Naija Property AI", page_icon="🏠", layout="centered")

# --- SESSION STATE SETUP ---
if 'signed_in' not in st.session_state:
    st.session_state.signed_in = False

# --- WELCOME SCREEN ---
if not st.session_state.signed_in:
    st.title("🏠 Welcome to DreamHome Nigeria")
    st.markdown("### Get an instant Market Value estimate for any property.")
    
    with st.form("user_details"):
        name = st.text_input("What is your name?")
        state = st.selectbox("Select your State", ["Lagos", "Abuja", "Imo", "Rivers", "Oyo", "Kano", "Enugu"])
        submit = st.form_submit_button("Start Application")
        
        if submit and name:
            st.session_state.signed_in = True
            st.session_state.user_name = name
            st.session_state.user_state = state
            st.rerun()

# --- MAIN DASHBOARD ---
if st.session_state.signed_in:
    st.title(f"Welcome, {st.session_state.user_name}! 👋")
    st.write(f"Analyzing real estate data for {st.session_state.user_state}.")
    
    # AI Prediction Section
    st.markdown("---")
    st.subheader("🤖 AI Price Prediction")
    house_type = st.selectbox("House Type", ["Bungalow", "Duplex", "Mansion", "Flat"])
    bedrooms = st.slider("Number of Bedrooms", 1, 10, 3)
    
    if st.button("Predict Price"):
        # Basic prediction math
        base_price = 15000000
        if house_type == "Duplex": base_price *= 2
        if house_type == "Mansion": base_price *= 4
        price = base_price + (bedrooms * 2500000)
        st.success(f"Estimated Market Value: ₦{price:,.2f}")

    # Live Web Scraping Section
    st.markdown("---")
    st.subheader(f"🏘️ Real-time Listings in {st.session_state.user_state}")
    st.info("Fetching real data directly from PropertyPro.ng")
    
    if st.button("Fetch Live Market Data"):
        with st.spinner("Searching the web..."):
            df_live = get_live_prices(st.session_state.user_state)
            
            if df_live is not None and not df_live.empty:
                st.write("Here are the latest 5 properties currently for sale:")
                st.table(df_live)
            else:
                st.error("Could not find live data right now. Try selecting a different state like Lagos or Abuja.")
