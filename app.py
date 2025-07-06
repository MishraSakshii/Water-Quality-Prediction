import pandas as pd
import numpy as np
import joblib
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from io import BytesIO
from reportlab.pdfgen import canvas

# Load model and required files
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# Load station location data
try:
    station_df = pd.read_csv("station_locations.csv")  # Must contain: id, name, latitude, longitude
except:
    station_df = pd.DataFrame(columns=['id', 'name', 'latitude', 'longitude'])

# UI
st.title("💧 Water Pollutants Predictor ")
st.write("Predict water pollutant levels based on Year, Station ID, and Season")

# Inputs
year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2026)
station_id = st.text_input("Enter Station ID", value='1')
season = st.selectbox("Select Season", ["Summer", "Monsoon", "Winter", "Post-Monsoon"])

season_map = {"Summer": 1, "Monsoon": 2, "Winter": 3, "Post-Monsoon": 4}
season_val = season_map[season]

if st.button('Predict'):
    if not station_id:
        st.warning('Please enter the station ID')
    else:
        # Prepare input
        input_df = pd.DataFrame({'year': [year_input], 'id': [station_id], 'season': [season_val]})
        input_encoded = pd.get_dummies(input_df, columns=['id'])

        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # Predict
        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ['O2', 'NO3', 'NO2', 'SO4', 'PO4', 'CL']
        predicted_values = dict(zip(pollutants, predicted_pollutants))

        st.subheader(f"📍 Predicted pollutant levels for Station '{station_id}' in {year_input} ({season}):")
        result_df = pd.DataFrame(predicted_values.items(), columns=["Pollutant", "Level"])
        st.table(result_df)

        # Chart
        fig, ax = plt.subplots()
        ax.bar(result_df["Pollutant"], result_df["Level"], color='skyblue')
        ax.set_ylabel("Concentration")
        ax.set_title("Predicted Pollutant Levels")
        st.pyplot(fig)

        # WQI Calculation
        wqi = (
            predicted_values['O2'] * 0.2 -
            predicted_values['NO3'] * 0.2 -
            predicted_values['NO2'] * 0.15 -
            predicted_values['SO4'] * 0.15 -
            predicted_values['PO4'] * 0.15 -
            predicted_values['CL'] * 0.15
        )

        if wqi > 50:
            category = "Excellent"; color = "🟢"
        elif 30 < wqi <= 50:
            category = "Good"; color = "🟡"
        elif 10 < wqi <= 30:
            category = "Poor"; color = "🟠"
        else:
            category = "Very Poor"; color = "🔴"

        st.markdown("### ✅ Water Quality Classification")
        st.success(f"{color} Water Quality: **{category}** (WQI: {wqi:.2f})")

        st.markdown("### 📌 Recommendations")
        if category in ["Poor", "Very Poor"]:
            st.warning("⚠️ Not suitable for drinking. Immediate treatment recommended.")
        else:
            st.info("✅ Water quality is acceptable. Continue monitoring.")

        # Export to CSV
        csv_data = pd.DataFrame([{
            "Year": year_input,
            "Station ID": station_id,
            "Season": season,
            "WQI": round(wqi, 2),
            "Category": category,
            **predicted_values
        }])
        st.download_button(
            label="📄 Download CSV",
            data=csv_data.to_csv(index=False).encode('utf-8'),
            file_name=f"pollutants_{station_id}_{year_input}.csv",
            mime="text/csv"
        )

        # Export to PDF
        def generate_pdf(data_dict):
            buffer = BytesIO()
            c = canvas.Canvas(buffer)
            c.setFont("Helvetica", 12)
            c.drawString(100, 800, f"Water Quality Report - Station {station_id} ({season}, {year_input})")
            y = 770
            for k, v in data_dict.items():
                c.drawString(100, y, f"{k}: {v}")
                y -= 20
            c.save()
            buffer.seek(0)
            return buffer

        pdf_data = {
            "Year": year_input,
            "Station ID": station_id,
            "Season": season,
            "WQI": round(wqi, 2),
            "Category": category,
            **predicted_values
        }
        st.download_button(
            label="📄 Download PDF",
            data=generate_pdf(pdf_data),
            file_name=f"report_{station_id}_{year_input}.pdf",
            mime="application/pdf"
        )

        

