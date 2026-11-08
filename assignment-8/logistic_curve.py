import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Assignment 8 Problem 5. Logistic Curve")

beta0 = st.slider("beta_0 - Intercept", -10.0, 10.0, 0.0, 0.1)
beta1 = st.slider("beta_1 - Slope", -10.0, 10.0, 1.0, 0.1)

x = np.linspace(-10, 10, 1000)
eta = beta0 + beta1 * x
y = 1 / (1 + np.exp(-np.clip(eta, -500, 500)))

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("X")
ax.set_ylabel("f(x)")
ax.set_ylim(0, 1)
st.pyplot(fig)
