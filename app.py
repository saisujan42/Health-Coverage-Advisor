import streamlit as st
import pandas as pd
import pickle
import numpy as np

st.markdown(
    """
    <div>
        <center><h1>Medical Cost Predictor</h1></center>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("### Information of the beneficiary")
model = pickle.load(open("Model/model.pkl", "rb"))

input_data = []
# Age
input_data.append(st.slider("Enter his/her age", 0, 100))

# Sex
S = st.radio("Gender of beneficiary", ("Male", "Female"))
S_result = 1 if S == "Male" else 0
input_data.append(S_result)

# BMI
input_data.append(st.text_input("Enter his/her BMI"))

# Children
child = st.selectbox("How many children does he/she have?", [0, 1, 2, 3, 4, 5])
input_data.append(child)

# Smoke
D = st.radio("Does he/she smoke?", ("Yes", "No"))
D_result = 1 if D == "Yes" else 0
input_data.append(D_result)

# Region
R = st.selectbox(
    "Select the region", ("Northeast", "Northwest", "Southeast", "Southwest")
)
R_res = ["Northeast", "Northwest", "Southeast", "Southwest"].index(R)
input_data.append(R_res)

# Insurance coverage (used for calculation but not part of the model input)
se = st.text_input("Insurance coverage (Min: 100000)") 
try:
    se = float(se)
except ValueError:
    st.error("Please enter a valid insurance coverage amount.")
    se = 0

# Calculation based on the insurance coverage
erri = se // 100000  # This gives the coverage amount in millions

# Prediction
try:
    if st.button("Predict"):
        # Model expects 6 features; insurance coverage is not included
        p = model.predict([input_data])
        
        # Custom calculation based on prediction and insurance coverage
        if child == 0:
            ans = (round(float(p[0]), 2) * erri) / 4
        else:
            ans = (((round(float(p[0]), 2) * erri) / 4) * (child / 2))
        st.success(f"The estimated medical cost is {ans} INR")
except Exception as e:
    st.error(f"An error occurred: {e}")
