import streamlit as st
import numpy as np
import pickle
import os
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Diet AI",
    page_icon="🥗",
    layout="wide"
)

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "images", "img.png")

# ---------- SIDEBAR STYLE ----------
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    padding: 10px;
}
section[data-testid="stSidebar"] img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

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
    st.error("Model not loaded. Check .pkl file and dependencies.")
    st.stop()

# ---------- RESET BUTTON ----------
if st.sidebar.button("Reset"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ---------- SIDEBAR IMAGE ----------
if os.path.exists(IMAGE_PATH):
    st.sidebar.image(IMAGE_PATH, width=160)

# ---------- SIDEBAR ----------
st.sidebar.header("User Profile")

age = st.sidebar.number_input("Age", 10, 100, value=22, key="age")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"], key="gender")

height = st.sidebar.number_input("Height (cm)", 100.0, 250.0, 170.0, key="height")

weight = st.sidebar.number_input("Weight (kg)", 30.0, 200.0, 65.0, key="weight")

bmi = st.sidebar.slider("Current BMI", 10.0, 50.0, 22.0, key="bmi")

activity = st.sidebar.select_slider("Activity Level", ["Low", "Moderate", "High"], key="activity")

sugar = st.sidebar.number_input("Sugar Level", 50.0, 300.0, 120.0, key="sugar")

cholesterol = st.sidebar.number_input("Cholesterol", 100.0, 400.0, 200.0, key="cholesterol")

goal = st.sidebar.selectbox("Primary Goal", ["Weight Loss", "Maintain", "Muscle Gain"], key="goal")

# ---------- MAPPINGS ----------
gender_map = {"Male": 0, "Female": 1}
activity_map = {"Low": 0, "Moderate": 1, "High": 2}
goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

# ---------- DIET INFO ----------
diet_info = {
    0: {"name": "Low Carb Diet", "icon": "🥦", "color": "#2ecc71", "desc": "High protein and low sugar diet."},
    1: {"name": "Diabetic Diet", "icon": "🥗", "color": "#3498db", "desc": "Balanced meals to control blood sugar."},
    2: {"name": "Heart Healthy Diet", "icon": "❤️", "color": "#e74c3c", "desc": "Low fat and heart friendly foods."},
    3: {"name": "Balanced Diet", "icon": "🍽️", "color": "#f1c40f", "desc": "All nutrients in proper proportion."},
    4: {"name": "High Protein Diet", "icon": "💪", "color": "#9b59b6", "desc": "Supports muscle growth and recovery."}
}

# ---------- UI STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2f3, #dfe9f3);
}
.main-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
    color: #333;
}
.sub-text {
    text-align: center;
    color: #666;
    margin-bottom: 20px;
}
.result-card {
    background: white;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
    margin-top: 20px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}
.stat-pill {
    display: inline-block;
    padding: 6px 12px;
    background: #f1f1f1;
    border-radius: 20px;
    margin: 5px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🥗 Smart Diet AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Personalized Nutrition Plans using Machine Learning</div>", unsafe_allow_html=True)

# ---------- BUTTON ----------
if st.sidebar.button("Generate Plan"):

    with st.spinner("Analyzing your data..."):
        time.sleep(1)

        input_data = np.array([[age, gender_map[gender], height, weight, bmi,
                                activity_map[activity], sugar, cholesterol, goal_map[goal]]])

        prediction = model.predict(input_data)[0]
        result = diet_info.get(prediction, diet_info[3])

    st.markdown(f"""
    <div style="text-align:center;">
        <span class="stat-pill">Age: {age}</span>
        <span class="stat-pill">BMI: {bmi}</span>
        <span class="stat-pill">Goal: {goal}</span>
    </div>

    <div class="result-card">
        <h2 style="color:{result['color']};">{result['icon']} {result['name']}</h2>
        <p>{result['desc']}</p>
        <p style="font-size:13px; color:#888;">Based on {activity} activity level</p>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

else:
    st.info("Fill the details from sidebar and click Generate Plan")
