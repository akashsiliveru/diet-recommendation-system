```python
import streamlit as st
import numpy as np
import pickle
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- CONFIG ----------
st.set_page_config(page_title="Smart Diet AI", page_icon="🥗", layout="wide")

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

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

# ---------- CSS (PREMIUM UI) ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2f7, #dfe9f3);
}

.header {
    text-align:center;
    font-size:42px;
    font-weight:800;
}

.sub {
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    padding:20px;
    border-radius:20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

.metric-card {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='header'>🥗 Smart Diet AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Your Personal AI Nutrition Coach</div>", unsafe_allow_html=True)

# ---------- INPUT SECTION ----------
with st.container():
    st.markdown("### 👤 Enter Your Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=10, max_value=100, value=None)
        gender = st.selectbox("Gender", ["Select", "Male", "Female"])

    with col2:
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=None)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=None)

    with col3:
        activity = st.selectbox("Activity", ["Low", "Moderate", "High"])
        goal = st.selectbox("Goal", ["Select", "Weight Loss", "Maintain", "Muscle Gain"])

    sugar = st.number_input("Sugar Level", min_value=50.0, max_value=300.0, value=None)
    cholesterol = st.number_input("Cholesterol", min_value=100.0, max_value=400.0, value=None)

# ---------- BMI ----------
if height and weight:
    bmi = weight / ((height / 100) ** 2)
else:
    bmi = 0

# ---------- METRICS ----------
st.markdown("### 📊 Health Overview")

c1, c2, c3 = st.columns(3)
c1.metric("BMI", f"{bmi:.2f}" if bmi else "--")
c2.metric("Sugar", f"{sugar}" if sugar else "--")
c3.metric("Cholesterol", f"{cholesterol}" if cholesterol else "--")

# ---------- BMI GAUGE ----------
if bmi:
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

# ---------- BUTTON ----------
generate = st.button("🚀 Generate Plan")

# ---------- MAPPING ----------
gender_map = {"Male": 0, "Female": 1}
activity_map = {"Low": 0, "Moderate": 1, "High": 2}
goal_map = {"Weight Loss": 0, "Maintain": 1, "Muscle Gain": 2}

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

# ---------- GENERATE ----------
if generate:

    if not all([age, height, weight, sugar, cholesterol]) \
        or gender == "Select" or goal == "Select":
        st.warning("⚠️ Please fill all fields")
        st.stop()

    input_data = np.array([[age, gender_map[gender], height, weight, bmi,
                            activity_map[activity], sugar, cholesterol, goal_map[goal]]])

    prediction = model.predict(input_data)[0]
    result = diet_info.get(prediction)

    diet_name = result["name"]

    # ---------- RESULT ----------
    st.markdown(f"""
    <div class="card">
        <h2 style="text-align:center;color:{result['color']}">
        🥗 {diet_name}
        </h2>
        <p style="text-align:center;">
        Personalized recommendation based on your health data
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- WHY ----------
    st.markdown("### 🧠 Why this recommendation?")
    st.info(f"""
    Your BMI is {bmi:.2f}, sugar level is {sugar},
    and cholesterol is {cholesterol}.
    Based on these, this diet is optimal for your goal.
    """)

    # ---------- MEAL PLAN ----------
    st.markdown("### 🍽 Daily Plan")

    for meal, food in zip(["Breakfast", "Lunch", "Dinner"], diet_plans[diet_name]):
        st.markdown(f"""
        <div class="card">
            <h4>{meal}</h4>
            <p>{food}</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------- CALORIES ----------
    st.markdown("### 📊 Calories Distribution")

    chart_data = pd.DataFrame({
        "Meal": ["Breakfast", "Lunch", "Dinner"],
        "Calories": [400, 600, 500]
    })

    fig = px.bar(chart_data, x="Meal", y="Calories", color="Meal")
    st.plotly_chart(fig, use_container_width=True)

    st.success("Stay healthy 💚")
    st.balloons()

else:
    st.info("Fill your details and click Generate Plan 🚀")
```

