import streamlit as st
import numpy as np
import pickle
import os
import plotly.graph_objects as go
import base64
import random

# ---------- CONFIG ----------
st.set_page_config(page_title="Arogya Plan", page_icon="🥗", layout="wide")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")
BG_PATH = os.path.join(BASE_DIR, "assets", "images", "bg1.png")

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
    st.error("❌ Model failed to load")
    st.stop()

# ---------- BACKGROUND ----------
def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

bg = get_base64_image(BG_PATH)

if bg:
    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/png;base64,{bg}") no-repeat center center fixed;
        background-size: cover;
    }}

    .stApp::before {{
        content:"";
        position:fixed;
        inset:0;
        background:rgba(0,0,0,0.55);
        backdrop-filter:blur(3px);
        z-index:-1;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------- CSS ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    color: white !important;
}

/* Labels */
label, .stRadio label, .stSelectbox label, .stNumberInput label {
    color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* Header */
.header-box{
    text-align:center;
    padding:20px;
    margin-bottom:20px;
    background:rgba(0,0,0,0.35);
    border-radius:20px;
    backdrop-filter: blur(10px);
}

/* Main Title */
.main-title{
    font-size:48px;
    font-weight:800;
    background:linear-gradient(135deg,#ff7e00,#ff3c00);
    -webkit-background-clip:text;
    color:transparent;
    text-shadow:0 0 12px rgba(255,120,0,0.35);
}

/* Result Title */
.result-title{
    text-align:center;
    font-size:38px;
    font-weight:800;
    color:#ffb347 !important;
    margin:15px 0;
}

/* Section Heading */
.section-title{
    font-size:28px;
    font-weight:700;
    color:white !important;
    margin-top:20px;
    margin-bottom:10px;
}

/* Cards */
.card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding:20px;
    border-radius:20px;
    margin-bottom:15px;
    border:1px solid rgba(255,255,255,0.10);
}

/* Meal title */
.meal-head{
    font-size:24px;
    font-weight:700;
    color:white !important;
    margin-bottom:10px;
}

/* Meal text */
.meal-text{
    font-size:20px;
    font-weight:600;
    color:#FFD580 !important;
    line-height:1.9;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff7e00, #ff3c00);
    color: white !important;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# ---------- HEADER ----------
st.markdown("""
<div class="header-box">
<div class="main-title">🥗 Arogya Plan</div>
<p style="color:#dddddd;font-size:18px;">AI-powered personalized nutrition system</p>
</div>
""", unsafe_allow_html=True)

# ---------- INPUT ----------
if not st.session_state.submitted:

    st.markdown('<div class="section-title">👤 Enter Your Details</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", 10, 100)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        diet_pref = st.selectbox("Diet Preference", ["Veg", "Non-Veg"])

    with c2:
        height = st.number_input("Height (cm)", 100.0, 250.0)
        weight = st.number_input("Weight (kg)", 30.0, 200.0)
        region = st.selectbox("Food Style", ["South Indian", "North Indian"])

    with c3:
        activity = st.radio("Activity Level", ["Low", "Moderate", "High"], horizontal=True)
        goal = st.radio("Goal", ["Weight Loss", "Maintain", "Muscle Gain"], horizontal=True)
        budget = st.selectbox("Budget", ["Budget", "Premium"])

    sugar = st.number_input("Sugar Level", 50.0, 300.0)
    cholesterol = st.number_input("Cholesterol", 100.0, 400.0)

    if st.button("🚀 Generate Plan"):
        st.session_state.submitted = True
        st.session_state.data = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "diet_pref": diet_pref,
            "region": region,
            "budget": budget,
            "activity": activity,
            "goal": goal,
            "sugar": sugar,
            "cholesterol": cholesterol
        }
        st.rerun()

# ---------- OUTPUT ----------
if st.session_state.submitted:

    d = st.session_state.data
    bmi = d["weight"] / ((d["height"] / 100) ** 2)

    gender_map = {"Male": 0, "Female": 1}
    activity_map = {"Low": 0, "Moderate": 1, "High": 2}
    goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

    input_data = np.array([[
        d["age"],
        gender_map[d["gender"]],
        d["height"],
        d["weight"],
        bmi,
        activity_map[d["activity"]],
        d["sugar"],
        d["cholesterol"],
        goal_map[d["goal"]]
    ]])

    pred = model.predict(input_data)[0]

    diet_names = {
        0: "Low Carb Diet",
        1: "Diabetic Diet",
        2: "Heart Healthy Diet",
        3: "Balanced Diet",
        4: "High Protein Diet"
    }

    diet_name = diet_names.get(pred, "Balanced Diet")

    st.markdown(f'<div class="result-title">🥗 {diet_name}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", f"{bmi:.2f}")
    c2.metric("Sugar", f'{d["sugar"]:.1f}')
    c3.metric("Cholesterol", f'{d["cholesterol"]:.1f}')

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={"text": "BMI"},
        gauge={
            "axis": {"range": [10, 50]},
            "steps": [
                {"range": [10, 18], "color": "lightblue"},
                {"range": [18, 25], "color": "green"},
                {"range": [25, 30], "color": "orange"},
                {"range": [30, 50], "color": "red"},
            ]
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

    foods = {
        "Breakfast": {
            "Veg": ["🥣 Oats", "🥞 Dosa", "🥪 Veg Sandwich", "🍎 Fruits", "🥛 Milk"],
            "Non-Veg": ["🥚 Eggs", "🍗 Chicken Sandwich", "🍳 Omelette", "🥛 Milk", "🍌 Banana"]
        },
        "Lunch": {
            "Veg": ["🍚 Rice + Dal", "🥗 Salad", "🫓 Roti + Curry", "🥘 Veg Biryani"],
            "Non-Veg": ["🍗 Chicken Rice", "🐟 Fish Curry", "🍖 Egg Rice", "🍚 Rice + Chicken Curry"]
        },
        "Dinner": {
            "Veg": ["🥣 Soup", "🫓 Roti + Paneer", "🥗 Salad Bowl", "🍲 Khichdi"],
            "Non-Veg": ["🍗 Grilled Chicken", "🐟 Fish Fry", "🥚 Egg Curry", "🍲 Chicken Soup"]
        },
        "Snacks": {
            "Veg": ["🥜 Nuts", "🍎 Apple", "🍌 Banana", "🥒 Cucumber"],
            "Non-Veg": ["🥚 Boiled Eggs", "🥜 Nuts", "🍌 Banana"]
        },
        "Drinks": {
            "Veg": ["🥤 Buttermilk", "🍵 Green Tea", "🥛 Milk", "🍋 Lemon Water"],
            "Non-Veg": ["🥤 Protein Shake", "🍵 Green Tea", "🥛 Milk"]
        }
    }

    st.markdown('<div class="section-title">🍽 Your Daily Plan</div>', unsafe_allow_html=True)

    for meal in ["Breakfast", "Lunch", "Dinner"]:
        options = random.sample(foods[meal][d["diet_pref"]], 3)

        st.markdown(f"""
        <div class="card">
            <div class="meal-head">{meal}</div>
            <div class="meal-text">
                ✅ {options[0]} <br>
                ✅ {options[1]} <br>
                ✅ {options[2]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    snack = random.choice(foods["Snacks"][d["diet_pref"]])
    drink = random.choice(foods["Drinks"][d["diet_pref"]])

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="meal-head">🥜 Snacks</div>
            <div class="meal-text">✅ {snack}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="meal-head">🥤 Drink</div>
            <div class="meal-text">✅ {drink}</div>
        </div>
        """, unsafe_allow_html=True)

    st.info(f"🍴 Selected: {d['diet_pref']} | {d['region']} | {d['budget']}")

    if st.button("🔄 Try Again"):
        st.session_state.submitted = False
        st.rerun()
