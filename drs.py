import streamlit as st
import numpy as np
import pickle
import os
import pandas as pd
import plotly.express as px

# ---------- CONFIG ----------
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
    except:
        return None

model = load_model()

if model is None:
    st.error("Model failed to load")
    st.stop()

# ---------- RESET ----------
if st.sidebar.button("🔄 Reset"):
    st.session_state.clear()
    st.rerun()

# ---------- SIDEBAR ----------
if os.path.exists(IMAGE_PATH):
    st.sidebar.image(IMAGE_PATH, width=130)

st.sidebar.markdown("## 👤 User Profile")

age = st.sidebar.number_input("Age", 10, 100, 22, key="age")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"], key="gender")
height = st.sidebar.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")
weight = st.sidebar.number_input("Weight (kg)", 30.0, 200.0, 65.0, key="weight")

# BMI
bmi = weight / ((height / 100) ** 2)
st.sidebar.markdown(f"### 🧮 BMI: {bmi:.2f}")

activity = st.sidebar.select_slider("Activity Level", ["Low", "Moderate", "High"], key="activity")
sugar = st.sidebar.number_input("Sugar Level", 50.0, 300.0, 120.0, key="sugar")
cholesterol = st.sidebar.number_input("Cholesterol", 100.0, 400.0, 200.0, key="cholesterol")
goal = st.sidebar.selectbox("Primary Goal", ["Weight Loss", "Maintain", "Muscle Gain"], key="goal")

# ---------- MAPPING ----------
gender_map = {"Male": 0, "Female": 1}
activity_map = {"Low": 0, "Moderate": 1, "High": 2}
goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

# ---------- DIET DATA ----------
diet_info = {
    0: {"name": "Low Carb Diet", "color": "#27ae60"},
    1: {"name": "Diabetic Diet", "color": "#2980b9"},
    2: {"name": "Heart Healthy Diet", "color": "#c0392b"},
    3: {"name": "Balanced Diet", "color": "#f39c12"},
    4: {"name": "High Protein Diet", "color": "#8e44ad"}
}

diet_plans = {
    "Low Carb Diet": ["🥚 Eggs", "🍗 Chicken", "🥗 Salad"],
    "Diabetic Diet": ["🥣 Oats", "🍚 Brown Rice", "🥦 Veggies"],
    "Heart Healthy Diet": ["🍎 Fruits", "🐟 Fish", "🥜 Nuts"],
    "Balanced Diet": ["🍚 Rice", "🥘 Dal", "🥦 Curry"],
    "High Protein Diet": ["🧀 Paneer", "🍗 Chicken", "🥤 Protein Shake"]
}

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #e6ecf5);
}

/* HEADER */
.header {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #2c3e50;
}

.sub {
    text-align: center;
    color: #7f8c8d;
    margin-bottom: 20px;
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {
    .header {
        font-size: 28px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='header'>🥗 Smart Diet AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>AI-powered personalized nutrition system</div>", unsafe_allow_html=True)

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)
col1.metric("BMI", f"{bmi:.2f}")
col2.metric("Sugar", f"{sugar}")
col3.metric("Cholesterol", f"{cholesterol}")

# ---------- BUTTON ----------
generate = st.sidebar.button("🚀 Generate Plan")

if generate:

    input_data = np.array([[age, gender_map[gender], height, weight, bmi,
                            activity_map[activity], sugar, cholesterol, goal_map[goal]]])

    prediction = model.predict(input_data)[0]
    result = diet_info.get(prediction)

    diet_name = result["name"]

    # RESULT CARD
    st.markdown(f"""
    <div class="card">
        <h2 style="text-align:center; color:{result['color']}">
            🥗 {diet_name}
        </h2>
        <p style="text-align:center;">
            Personalized recommendation based on your health data
        </p>
    </div>
    """, unsafe_allow_html=True)

    # DIET PLAN
    st.markdown("### 🍽 Daily Plan")

    df = pd.DataFrame({
        "Meal": ["Breakfast", "Lunch", "Dinner"],
        "Food": diet_plans[diet_name]
    })

    st.dataframe(df, use_container_width=True)

    # ---------- ANIMATED CHART ----------
    st.markdown("### 📊 Calories Distribution")

    chart_data = pd.DataFrame({
        "Meal": ["Breakfast", "Lunch", "Dinner"],
        "Calories": [400, 600, 500]
    })

    fig = px.bar(chart_data, x="Meal", y="Calories",
                 color="Meal",
                 title="Daily Calories")

    st.plotly_chart(fig, use_container_width=True)

    st.success("Stay healthy 💚")

else:
    st.info("Fill your details and click Generate Plan")
