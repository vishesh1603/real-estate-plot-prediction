"""
Real Estate Plot / Property Price Predictor
Streamlit demo app — loads the trained model from notebook 04_modeling.ipynb
and lets a user enter property characteristics to get a live price estimate.

Run with:
    streamlit run app/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Plot Price Predictor", page_icon="🏡", layout="centered")

# ---------------------------------------------------------------------------
# Load model artifacts (produced by notebooks 03 and 04)
# ---------------------------------------------------------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/best_model.pkl")
    scaler = joblib.load("models/scaler.pkl")
    feature_cols = joblib.load("models/feature_columns.pkl")
    return model, scaler, feature_cols

model, scaler, feature_cols = load_artifacts()

# Use exactly the columns the scaler was fit on (avoids feature-name mismatches)
NUMERIC_COLS = list(scaler.feature_names_in_)

CITIES = ["Chandigarh", "Ghaziabad", "Lucknow", "Pune"]
PROPERTY_TYPES = ["Builderfloor", "Plot", "Villa"]
FACINGS = ["Unknown", "North", "Northeast", "East", "Southeast",
           "South", "Southwest", "West", "Northwest"]

st.title("🏡 Real Estate Price Predictor")
st.caption("Enter property details to get an AI-estimated market price, based on listings across "
           "Chandigarh, Ghaziabad, Lucknow, and Pune.")

st.divider()

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    city = st.selectbox("City", CITIES)
    property_type = st.selectbox("Property Type", PROPERTY_TYPES)
    area = st.number_input("Area (sq.ft.)", min_value=100, max_value=20000, value=1000, step=50)
    facing = st.selectbox("Facing Direction", FACINGS)
    age_of_property = st.number_input("Age of Property (years)", min_value=0, max_value=50, value=2)

with col2:
    security_deposit = st.number_input("Security Deposit (₹)", min_value=0, value=0, step=5000)
    locality_score = st.slider("Locality Score (1-10)", min_value=1.0, max_value=10.0, value=6.0, step=0.5)
    new_resale = st.radio("New or Resale", ["New", "Resale"], horizontal=True)
    price_negotiable = st.radio("Price Negotiable?", ["Yes", "No"], horizontal=True)
    furnished = st.radio("Furnished?", ["Yes", "No"], horizontal=True)

st.subheader("Amenities")
amenity_labels = [
    "Lift(s)", "Full Power Backup", "24 X 7 Security", "Children's play area",
    "Club House", "Gymnasium", "Swimming Pool", "Sports Facility",
    "Jogging Track", "Landscaped Gardens", "Car Parking",
]
amenity_cols_ui = st.columns(3)
amenity_values = {}
for i, label in enumerate(amenity_labels):
    with amenity_cols_ui[i % 3]:
        amenity_values[label] = st.checkbox(label, value=False)

st.divider()

# ---------------------------------------------------------------------------
# Build feature row matching training schema exactly
# ---------------------------------------------------------------------------
def build_input_row():
    row = {c: 0 for c in feature_cols}

    row["area"] = area
    row["security_deposit"] = security_deposit
    row["age of property"] = age_of_property
    row["locality_score"] = locality_score
    row["new/resale"] = 1 if new_resale == "New" else 0
    row["price_negotiable"] = 1 if price_negotiable == "Yes" else 0
    row["furnished"] = 1 if furnished == "Yes" else 0

    amenity_count = 0
    for label, checked in amenity_values.items():
        val = 1 if checked else 0
        if label in row:
            row[label] = val
            if label != "Car Parking":  # amenity_count mirrors notebook 1's definition (10 core amenities)
                amenity_count += val
    row["amenity_count"] = amenity_count

    city_col = f"city_{city}"
    if city_col in row:
        row[city_col] = 1

    type_col = f"property_type_{property_type}"
    if type_col in row:
        row[type_col] = 1

    facing_col = f"facing_{facing}"
    if facing_col in row:
        row[facing_col] = 1

    row["status_Unknown"] = 1  # default: status not specified via this form

    ordered = pd.DataFrame([[row[c] for c in feature_cols]], columns=feature_cols)
    return ordered

if st.button("Predict Price", type="primary", use_container_width=True):
    input_df = build_input_row()

    numeric_present = [c for c in NUMERIC_COLS if c in input_df.columns]
    input_df[numeric_present] = scaler.transform(input_df[numeric_present])

    pred_log_price = model.predict(input_df)[0]
    pred_price = float(np.expm1(pred_log_price))
    pred_price = max(pred_price, 0)

    st.success(f"### Estimated Price: ₹ {pred_price:,.0f}")
    price_per_sqft = pred_price / area if area else 0
    st.caption(f"≈ ₹ {price_per_sqft:,.0f} per sq.ft.")

    st.info(
        "This is a model estimate based on historical listing data — actual market price "
        "may vary with negotiation, exact locality, and current demand conditions."
    )

st.divider()
st.caption("Model: trained in `notebooks/04_modeling.ipynb` · Data: merged listings across 4 cities "
           "(see `data_dictionary.md`)")
