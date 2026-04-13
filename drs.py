import streamlit as st
import numpy as np
import pickle
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Diet AI", page_icon="🥗", layout="wide")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images", "img.png")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

if model is None:
    st.stop()

# ---------- RESET ----------
if st.sidebar.button("Reset"):
    st.session_state.clear()
    st.rerun()

# ---------- SIDEBAR IMAGE ----------
if os.path.exists(IMAGE_PATH):
    st.sidebar.image(IMAGE_PATH, width=150)

st.sidebar.header("User Profile")

# ---------- INPUTS ----------
age = st.sidebar.number_input("Age", 10, 100, 22, key="age")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"], key="gender")
height = st.sidebar.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")
weight = st.sidebar.number_input("Weight (kg)", 30.0, 200.0, 65.0, key="weight")

# ✅ AUTO BMI
bmi = weight / ((height / 100) ** 2)
st.sidebar.markdown(f"**BMI:** {bmi:.2f}")

activity = st.sidebar.select_slider("Activity Level", ["Low", "Moderate", "High"], key="activity")
sugar = st.sidebar.number_input("Sugar Level", 50.0, 300.0, 120.0, key="sugar")
cholesterol = st.sidebar.number_input("Cholesterol", 100.0, 400.0, 200.0, key="cholesterol")
goal = st.sidebar.selectbox("Primary Goal", ["Weight Loss", "Maintain", "Muscle Gain"], key="goal")

# ---------- MAP ----------
gender_map = {"Male": 0, "Female": 1}
activity_map = {"Low": 0, "Moderate": 1, "High": 2}
goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

# ---------- DIET INFO ----------
diet_info = {
    0: {"name": "Low Carb Diet", "color": "#2ecc71"},
    1: {"name": "Diabetic Diet", "color": "#3498db"},
    2: {"name": "Heart Healthy Diet", "color": "#e74c3c"},
    3: {"name": "Balanced Diet", "color": "#f1c40f"},
    4: {"name": "High Protein Diet", "color": "#9b59b6"}
}

# ---------- DIET PLANS ----------
diet_plans = {
    "Low Carb Diet": ["Eggs", "Grilled Chicken", "Salad"],
    "Diabetic Diet": ["Oats", "Brown Rice", "Vegetables"],
    "Heart Healthy Diet": ["Fruits", "Fish", "Nuts"],
    "Balanced Diet": ["Rice", "Dal", "Veg Curry"],
    "High Protein Diet": ["Paneer", "Chicken", "Protein Shake"]
}

# ---------- HEADER ----------
st.title("🥗 Smart Diet AI")
st.caption("Personalized Nutrition Plans using Machine Learning")

# ---------- BUTTON ----------
if st.sidebar.button("Generate Plan"):

    input_data = np.array([[age, gender_map[gender], height, weight, bmi,
                            activity_map[activity], sugar, cholesterol, goal_map[goal]])

    prediction = model.predict(input_data)[0]
    result = diet_info.get(prediction)

    diet_name = result["name"]

    # ---------- RESULT ----------
    st.success(f"Recommended Diet: {diet_name}")

    # ---------- EXPLANATION ----------
    st.subheader("Why this diet?")
    st.write(f"Based on your BMI ({bmi:.2f}), activity level ({activity}), and goal ({goal}), this diet is suitable.")

    # ---------- DIET PLAN ----------
    st.subheader("Your Daily Diet Plan")

    meals = diet_plans[diet_name]

    diet_df = pd.DataFrame({
        "Meal": ["Breakfast", "Lunch", "Dinner"],
        "Food": meals
    })

    st.table(diet_df)

    # ---------- CALORIE CHART ----------
    st.subheader("Estimated Calories Distribution")

    calories = [400, 600, 500]

    fig, ax = plt.subplots()
    ax.bar(["Breakfast", "Lunch", "Dinner"], calories)
    ax.set_ylabel("Calories")

    st.pyplot(fig)

    st.balloons()

else:
    st.info("Fill details and click Generate Plan")
