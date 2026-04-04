import streamlit as st
import pandas as pd
from scraper import get_live_prices

st.set_page_config(page_title="Naija Property AI", page_icon="🏠", layout="centered")

if 'signed_in' not in st.session_state:
    st.session_state.signed_in = False

if not st.session_state.signed_in:
    st.title("🏠 Welcome to DreamHome Nigeria")
    st.markdown("### Get an instant Market Value estimate for any property.")
    with st.form("user_details"):
        name = st.text_input("Full Name", placeholder="e.g. Fide Nwaogu")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        location = st.selectbox("State", ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"])
        area = st.text_input("Specific Neighborhood/Area", placeholder="e.g. Naze, Ihiagwa, or Owerri")
        submit_button = st.form_submit_button("Access Predictor")
        if submit_button:
            if name and area:
                st.session_state.signed_in = True
                st.session_state.user_name = name
                st.session_state.user_area = area
                st.session_state.user_state = location
                st.rerun()
            else:
                st.error("Please provide your name and area to continue.")
else:
    st.sidebar.title("Active Session")
    st.sidebar.write(f"Client: {st.session_state.user_name}")
    st.sidebar.write(f"Location: {st.session_state.user_area}, {st.session_state.user_state}")
    if st.sidebar.button("Sign Out / New Search"):
        st.session_state.signed_in = False
        st.rerun()
    st.title("📊 Property Market Value Estimator")
    st.write(f"Current Market Analysis for: {st.session_state.user_area}")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        sqft = st.number_input("Total Land/Floor Area (sqft)", min_value=100, value=500, step=50)
        beds = st.slider("Number of Bedrooms", 1, 10, 3)
        condition = st.selectbox("Property Condition", ["Brand New", "Newly Renovated", "Fair / Standard", "Needs Major Renovation"])
    with col2:
        baths = st.slider("Number of Bathrooms", 1, 8, 3)
        prop_type = st.selectbox("Building Type", ["Flat/Apartment", "Bungalow", "Terrace", "Duplex"])
    with st.expander("➕ Add Premium Amenities (Optional)"):
        estate = st.checkbox("Inside a Secured Estate")
        borehole = st.checkbox("Dedicated Borehole / Good Water Supply")
        road = st.checkbox("Tarred Access Road")
    st.markdown("###")
    if st.button("Calculate Total Market Value (₦)", use_container_width=True):
        base_value = 8000000 
        sqft_val = sqft * 12000
        room_val = (beds * 4000000) + (baths * 1500000)
        raw_total = base_value + sqft_val + room_val
        type_mult = {"Flat/Apartment": 0.9, "Bungalow": 1.0, "Terrace": 1.15, "Duplex": 1.35}
        raw_total = raw_total * type_mult[prop_type]
        cond_mult = {"Brand New": 1.2, "Newly Renovated": 1.1, "Fair / Standard": 1.0, "Needs Major Renovation": 0.7}
        raw_total = raw_total * cond_mult[condition]
        if estate: raw_total += 5000000
        if borehole: raw_total += 1000000
        if road: raw_total += 3000000
        prem = 1.6 if st.session_state.user_state in ["Lagos", "FCT - Abuja"] else 1.0
        final_total = raw_total * prem
        st.balloons()
        st.success(f"## Estimated Purchase Price: ₦{final_total:,.2f}")
        st.markdown("#### 📑 Estimated Valuation Breakdown")
        b1, b2 = st.columns(2)
        with b1:
            st.info(f"Land & Location Value: \n₦{(final_total * 0.35):,.2f}")
        with b2:
            st.info(f"Structure & Amenities Value: \n₦{(final_total * 0.65):,.2f}")
        st.caption(f"💡 Estimated Rent: ₦{(final_total * 0.10):,.2f} per year.")

# --- LIVE DATA SECTION ---
st.markdown("---") 
st.subheader(f"🏠 Real-time Listings")

if st.button("Check PropertyPro.ng for Live Prices"):
    with st.spinner("Searching the web..."):
        # This calls the robot in your scraper.py file
        # We use 'Lagos' as a default if the state variable name is different in your code
        df_live = get_live_prices("Lagos") 
        
        if df_live is not None and not df_live.empty:
            st.write("Here are the latest 5 listings found:")
            st.table(df_live) 
        else:
            st.error("Could not find live data. Try again in a moment!")
