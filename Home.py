import streamlit as st
import pandas as pd

# Create a function to handle the Streamlit app logic
def streamlit_app():
    # Use Streamlit to create the UI components and logic
    st.title("Heatwave Risk Assessment")

    # Define the options and corresponding scores for each category
    building_types = {
        "Ground floor flat": -15,
        "Upper floor flats": 9,
        "Bungalow": -2,
        "Rest* cavity": -1,
        "Rest* solid": 4
    }
    location_types = {
        "Greenery nearby (0 °C UHI)": -3,
        "Some greenery nearby (1 °C UHI)": 2,
        "No greenery nearby (2 °C UHI)": 3
    }
    heatwave_durations = {
        "No heatwave year": -3,
        "1 day heatwave": 4,
        "3 days heatwave": 6,
        "5+ days heatwave": 9
    }
    years = {
        "Current": -2,
        "2030": 2,
        "2050": 5,
        "2080": 6
    }

    # Use Streamlit to create selection boxes for each category
    building_type = st.selectbox("Choose Building Type", options=list(building_types.keys()))
    location_type = st.selectbox("Choose Location", options=list(location_types.keys()))
    heatwave_duration = st.selectbox("Choose Heatwave Duration", options=list(heatwave_durations.keys()))
    year = st.selectbox("Choose Year", options=list(years.keys()))

    # Calculate the sum of scores
    total_score = (building_types[building_type] +
                   location_types[location_type] +
                   heatwave_durations[heatwave_duration] +
                   years[year])

    # Display the selected options and their scores
    st.write(f"Building Type Score: {building_types[building_type]}")
    st.write(f"Location Score: {location_types[location_type]}")
    st.write(f"Heatwave Duration Score: {heatwave_durations[heatwave_duration]}")
    st.write(f"Year Score: {years[year]}")
    st.markdown(f"**Total Score: {total_score}**")

   # Display risk assessment
    if total_score >= 5:
        st.error('At Risk')
    else:
        st.success('Not At Risk')
# This check ensures this code only runs when executing the script directly
# and not when importing it as a module.
if __name__ == "__main__":
    streamlit_app()
