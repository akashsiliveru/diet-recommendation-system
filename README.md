<div align="center">

# 🍃 Arogya Plan
### AI-Powered Personalized Diet Recommendation System

*"Because your body is unique — your diet should be too."*

<br/>

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org)
[![Status](https://img.shields.io/badge/Status-Completed-22c55e?style=for-the-badge)](.)

<br/>

> A premium end-to-end machine learning system that generates hyper-personalized diet plans  
> using real health metrics, fitness goals, lifestyle data, and intelligent KNN-based recommendations.

<br/>

[🚀 Live Demo](#-live-demo) · [📌 Problem Statement](#-problem-statement) · [🧠 ML Pipeline](#-ml-pipeline) · [📊 Features](#-features-used) · [🛠 Tech Stack](#️-tech-stack) · [📂 Project Structure](#-project-structure)

---

</div>

## 🚀 Live Demo

<div align="center">

### ✨ Experience the App

**🔗 [diet-recommendation-system-2drzcfznrwqxxtr2ou6vny.streamlit.app](https://diet-recommendation-system-2drzcfznrwqxxtr2ou6vny.streamlit.app/)**

*Enter your health profile → Get your personalized diet plan in seconds*

</div>

---

## 📌 Problem Statement

> **The diet industry is broken.** Generic meal plans fail because every individual is biochemically different.

Most diet charts today ignore that two people with the same weight-loss goal can need completely different nutrition strategies based on age, activity level, health conditions, and food preferences.

**Arogya Plan** solves this with an ML-powered engine that treats every user as a unique data point.

| Challenge | Our Approach |
|-----------|-------------|
| Generic meal plans | KNN-based personalized matching |
| Ignoring health conditions | Sugar & cholesterol-aware recommendations |
| One-size-fits-all goals | Multi-goal support (loss / gain / maintain / healthy) |
| Budget insensitivity | Budget-tier filtering (Normal / Premium) |
| Dietary restrictions ignored | Veg / Non-Veg preference handling |

---

## 🎯 Project Objectives

Build an intelligent recommendation engine that generates **fully customized meal plans** based on individual profiles, supporting four core fitness goals:

| Goal | Description |
|------|-------------|
| 🔥 **Weight Loss** | Calorie-deficit plans with lean nutrition |
| 💪 **Weight Gain** | High-protein, calorie-surplus meal plans |
| ⚖️ **Maintain Weight** | Balanced macros for weight stability |
| 🌿 **Healthy Lifestyle** | Nutrient-dense, wholesome everyday eating |

---

## 🧠 ML Pipeline

```
Raw User Input
      │
      ▼
┌─────────────────────────┐
│   Data Preprocessing     │  ← Encoding · Scaling · BMI Calculation
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│   KNN Model  (.pkl)      │  ← Finds k most similar user profiles
└─────────────────────────┘
      │
      ▼
┌─────────────────────────┐
│   Recommendation Engine  │  ← Breakfast · Lunch · Dinner · Snacks · Drinks
└─────────────────────────┘
      │
      ▼
  Personalized Meal Plan ✅
```

### Stage 1 — Data Collection
Structured dataset covering diverse user profiles including health parameters (BMI, sugar, cholesterol), meal types, caloric profiles, dietary preferences, fitness goals, activity levels, and budget constraints.

### Stage 2 — Preprocessing

| Step | Technique |
|------|-----------|
| Missing Values | Imputation / Removal |
| Categorical Data | Label Encoding |
| Feature Selection | Correlation Analysis |
| Scaling | StandardScaler / MinMaxScaler |
| BMI Derivation | Computed from height & weight |

### Stage 3 — Model: K-Nearest Neighbors (KNN)

KNN was selected as the backbone of the recommendation engine because:

- ✅ **Similarity-based logic** — naturally fits recommendation use cases
- ✅ **Profile matching** — finds users with nearest health & goal profiles
- ✅ **Non-parametric** — no assumption about data distribution
- ✅ **Interpretable** — easy to understand and communicate outputs
- ✅ **Fast inference** — real-time predictions on medium-scale data

### Stage 4 — Prediction Flow

```
User submits health profile  →  Encode + Scale input features
        ↓
KNN finds k nearest neighbor profiles  →  Aggregate best-matching meal plan
        ↓
Return structured diet recommendation ✅
```

---

## 📊 Features Used

| # | Feature | Type | Description |
|---|---------|------|-------------|
| 1 | **Age** | Numeric | User's age in years |
| 2 | **Gender** | Categorical | Male / Female |
| 3 | **Height** | Numeric | Height in centimetres |
| 4 | **Weight** | Numeric | Weight in kilograms |
| 5 | **BMI** | Derived | Body Mass Index (auto-calculated) |
| 6 | **Goal** | Categorical | Weight Loss / Gain / Maintain / Healthy |
| 7 | **Activity Level** | Categorical | Sedentary / Moderate / Active |
| 8 | **Food Type** | Categorical | Vegetarian / Non-Vegetarian |
| 9 | **Sugar Level** | Numeric | Blood sugar indicator |
| 10 | **Cholesterol** | Numeric | Cholesterol level |
| 11 | **Budget** | Categorical | Normal / Premium |

---

## 🍽️ Sample Output

```
┌──────────────────────────────────────────────────────┐
│              YOUR PERSONALIZED DIET PLAN              │
├──────────────┬───────────────────────────────────────┤
│ 🥣 Breakfast │  Oats with banana & almond milk       │
│ 🍛 Lunch     │  Brown rice, dal, stir-fried veggies  │
│ 🍲 Dinner    │  Grilled paneer, roti, salad          │
│ 🍎 Snacks    │  Mixed nuts & Greek yogurt            │
│ 🥤 Drinks    │  Green tea, warm lemon water          │
├──────────────┴───────────────────────────────────────┤
│ 🔥 Target Daily Calories:  1,850 kcal                │
└──────────────────────────────────────────────────────┘
```

---

## 📈 Evaluation Approach

Since Arogya Plan is a recommendation system, evaluation goes beyond standard accuracy metrics:

| Metric | What It Measures |
|--------|------------------|
| **Personalization Quality** | Are meals aligned with user's goal & profile? |
| **Similarity Accuracy** | Are nearest neighbors genuinely similar profiles? |
| **Meal Relevance** | Are recommendations realistic and diverse? |
| **Output Diversity** | Avoids repetitive / redundant suggestions |
| **Real-World Validation** | Manual testing across varied user personas |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.10 | Core development |
| **Data** | Pandas + NumPy | Manipulation & numerical operations |
| **ML** | Scikit-learn (KNN) | Recommendation engine |
| **Deployment** | Streamlit | Interactive web application |
| **Visualization** | Plotly | Charts & analytics |
| **UI** | HTML / CSS | Premium styling & layout |
| **Model Persistence** | Pickle (.pkl) | Saved model deployment |

---

## 📂 Project Structure

```
arogya-plan/
│
├── 📁 .streamlit/                  # Streamlit configuration
│   └── config.toml
│
├── 📁 assets/                      # Static assets (images, icons)
│
├── 📁 model/
│   └── 🤖 model.pkl                # Trained KNN model
│
├── 📁 notebooks/
│   ├── 📓 EDA.ipynb                # Exploratory Data Analysis
│   └── 📓 KNN_Model.ipynb          # Model training & evaluation
│
├── 🐍 drs.py                       # Main Streamlit application
├── 📋 requirements.txt             # Python dependencies
└── 📄 README.md                    # Project documentation
```

---

## ⚙️ Getting Started

**Prerequisites:** Python 3.10+, pip

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/diet-recommendation-system.git
cd diet-recommendation-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
streamlit run drs.py
```

Open `http://localhost:8501` in your browser.

---

## 🔮 Roadmap

- [ ] Regional Indian cuisine dataset expansion
- [ ] Weekly meal plan generation
- [ ] Macro/micronutrient breakdown per meal
- [ ] Calorie tracking dashboard
- [ ] Deep learning via collaborative filtering
- [ ] Multi-language support (Hindi, Telugu, Tamil)

---

<div align="center">

**Built with ❤️ for healthier living**

*If this project helped you, consider giving it a ⭐*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/diet-recommendation-system?style=social)](.)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/diet-recommendation-system?style=social)](.)

</div>
