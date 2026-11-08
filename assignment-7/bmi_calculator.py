import streamlit as st

st.title("BMI Calculator")

weight = st.number_input("Weight (lbs)", min_value=0, value=0)
feet = st.number_input("Height (ft)", min_value=0, value=0)
inches = st.number_input("Height (in)", min_value=0, max_value=11, value=0)

if st.button("Calculate BMI"):
    height = (feet * 12) + inches
    bmi = (weight / (height ** 2)) * 703
    st.write(f"BMI: {bmi:.1f}")