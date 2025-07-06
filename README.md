#  Water Quality Prediction - RMS

This project predicts **multiple water quality parameters** using machine learning techniques, with a focus on `MultiOutputRegressor` wrapped around a `RandomForestRegressor`. It was developed as part of a **one-month AICTE Virtual Internship sponsored by Shell in June 2025**.

---

## 🌍 Problem Statement

Access to clean water is a global priority. Traditional monitoring techniques are often manual, expensive, and time-consuming. This project aims to automate the **prediction of key water quality indicators** using real-world datasets and machine learning to support early pollution detection and proactive environmental management.

---

## 🔧 Technologies Used

- **Python 3.12**
- **Pandas, NumPy** – Data preprocessing and manipulation
- **Scikit-learn** – Model building and evaluation
- **Matplotlib, Seaborn** – Data visualization
- **Jupyter Notebook** – Exploratory development environment

---

## 📊 Target Parameters

The trained model predicts the following water quality indicators:

- **NH₄** (Ammonium)
- **BSK5 (BOD5)** – Biochemical Oxygen Demand
- **Colloids**
- **O₂** (Dissolved Oxygen)
- **NO₃**, **NO₂** – Nitrate and Nitrite
- **SO₄** – Sulfate
- **PO₄** – Phosphate
- **CL** – Chloride

---

## 🧠 Model Details

- **Model**: `MultiOutputRegressor(RandomForestRegressor())`
- **Input**: Preprocessed chemical and physical features
- **Output**: Simultaneous regression predictions for multiple parameters

---

## 📈 Evaluation Metrics

Model performance was evaluated using:

- **R² Score** – Measures goodness-of-fit
- **Mean Squared Error (MSE)** – Measures average squared difference between predicted and actual values

The model showed reliable performance across all predicted features.

---

## 📁 Trained Model Access

You can download the trained model file from the link below:

🔗 **[Download model (.pkl)](https://drive.google.com/file/d/18RJzu35vyuMgpcAE590u1IaDvHY3-SWq/view?usp=sharing)**

---

## 🚀 Future Enhancements

- Integration with a live water quality monitoring dashboard
- Inclusion of additional datasets for regional adaptability
- Cloud-based deployment using Flask or Streamlit
