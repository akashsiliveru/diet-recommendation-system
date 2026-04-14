import streamlit as st
import numpy as np
import pickle
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64

# ---------- CONFIG ----------
st.set_page_config(page_title="Arogya Plan", page_icon="🥗", layout="wide")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
BG_PATH = os.path.join(BASE_DIR, "assets", "images", "bg1.png")  # ✅ PNG

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

# ---------- BACKGROUND ----------
def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

bg_image = get_base64_image(BG_PATH)
file_ext = BG_PATH.split(".")[-1]

if bg_image:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/{file_ext};base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.55); /* lighter overlay */
        backdrop-filter: blur(3px);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Background image not found")

# ---------- GLOBAL CSS ----------
st.markdown("""
<style>

h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* RADIO FIX */
div[role="radiogroup"] {
    gap: 10px !important;
}

div.row-widget.stRadio > div {
    flex-direction: row;
    gap: 15px;
}

.stRadio {
    margin-bottom: -10px;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #ff7e00, #ff3c00);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    width: 250px;
}

.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- HEADER ----------
st.markdown("""
<div style="
text-align:center;
padding:20px;
margin-bottom:20px;
background: rgba(0,0,0,0.3);
border-radius:20px;
backdrop-filter: blur(10px);
">
<h1 style="
font-size:48px;
font-weight:800;
background: linear-gradient(135deg,#ff7e00,#ff3c00);
-webkit-background-clip: text;
color: transparent;
text-shadow: 0 0 20px rgba(255,120,0,0.6);
">
🥗 Arogya Plan
</h1>
<p style="color:#ccc;">
AI-powered personalized nutrition system
</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT ----------
if not st.session_state.submitted:

    st.markdown("### 👤 Enter Your Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=10, max_value=100)
        st.markdown("Gender")
        gender = st.radio("", ["Male", "Female"], horizontal=True)

    with col2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0)

    with col3:
        st.markdown("Activity Level")
        activity = st.radio("", ["Low", "Moderate", "High"], horizontal=True)

        st.markdown("Goal")
        goal = st.radio("", ["Weight Loss", "Maintain", "Muscle Gain"], horizontal=True)

    sugar = st.number_input("Sugar Level", min_value=50.0, max_value=300.0)
    cholesterol = st.number_input("Cholesterol", min_value=100.0, max_value=400.0)

    # 👉 CENTER BUTTON
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        generate = st.button("🚀 Generate Plan")

    if generate:

        if not all([age, height, weight, sugar, cholesterol]):
            st.warning("⚠️ Please fill all fields")
            st.stop()

        st.session_state.submitted = True
        st.session_state.data = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "activity": activity,
            "goal": goal,
            "sugar": sugar,
            "cholesterol": cholesterol
        }

        st.rerun()

# ---------- OUTPUT ----------
if st.session_state.submitted:

    data = st.session_state.data

    age = data["age"]
    gender = data["gender"]
    height = data["height"]
    weight = data["weight"]
    activity = data["activity"]
    goal = data["goal"]
    sugar = data["sugar"]
    cholesterol = data["cholesterol"]

    bmi = weight / ((height / 100) ** 2)

    gender_map = {"Male": 0, "Female": 1}
    activity_map = {"Low": 0, "Moderate": 1, "High": 2}
    goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

    input_data = np.array([[age, gender_map[gender], height, weight, bmi,
                            activity_map[activity], sugar, cholesterol, goal_map[goal]]])

    prediction = model.predict(input_data)[0]

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

    result = diet_info.get(prediction)
    diet_name = result["name"]

    st.markdown(f"<h2 style='text-align:center;color:#ff7e00;'>🥗 {diet_name}</h2>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", f"{bmi:.2f}")
    c2.metric("Sugar", f"{sugar}")
    c3.metric("Cholesterol", f"{cholesterol}")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={'text': "BMI"},
        gauge={
            'axis': {'range': [10, 50]},
            'steps': [
                {'range': [10, 18], 'color': "lightblue"},
                {'range': [18, 25], 'color': "green"},
                {'range': [25, 30], 'color': "orange"},
                {'range': [30, 50], 'color': "red"},
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🍽 Daily Plan")
    for meal, food in zip(["Breakfast", "Lunch", "Dinner"], diet_plans[diet_name]):
        st.markdown(f"""
        <div class="card">
            <h4>{meal}</h4>
            <p>{food}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 Try Again"):
        st.session_state.submitted = False
        st.rerun()

