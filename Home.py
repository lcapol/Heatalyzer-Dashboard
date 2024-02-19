import streamlit as st
import pandas as pd


building_types = {"Ground floor flats": "Ground floor flat",
                 "Mid floor flats": "Mid floor flat",
                  "Top floor flats": "Top floor flat",
                  "Bungalow houses": "Bungalow (detached)",
                  "Mid-terraced houses (non-bungalow) with cavity walls (post-1945)": "Mid terrace (Cavity/solid)",
                  "Mid-terraced houses (non-bungalow) with solid walls (pre-1945)": "Mid terrace (Solid/suspended)",
                  "End-terraced, Semi-detached, detached houses (non-bungalow) with cavity walls (post-1945)": "Compact house (semi-d)",
                  "End-erraced, Semi-detached, detached houses (non-bungalow) with solid walls (pre-1945)": "Medium house, solid (semi-d)"}

location_types =  {"Greenery nearby (0 °C UHI)": "",
                   "Some greenery nearby (1 °C UHI)": " + UHI 1",
                    "No greenery nearby (2 °C UHI)": " + UHI 2"}

heatwave_durations = {"No heatwave": ("", " RCP4.5"),
                      "1 day heatwave": " Heatwave",
                      "3 days heatwave": " Heatwave 3 days",
                      "5 days heatwave": " Heatwave 5 days",
                      "7 days heatwave": " Heatwave 7 days"}

years = {"Current": ("TMY", "2022"),
        "2030": "2030",
        "2050": "2050",
        "2080": "2080"}

#SET Degree hours input
file_path = 'data/SET_Max_dh_scoring.xlsx'

#Based on building location, heatwave duration and year create the scenario string for lookup in the xlsx file
def create_scenario(location_type, heatwave_duration, year):

    if year == "Current":
        if heatwave_duration == "No heatwave":
            scenario = years[year][0] + heatwave_durations[heatwave_duration][0]
        else:
            scenario = years[year][1]  + heatwave_durations[heatwave_duration]
    else:
        scenario = years[year]
        if heatwave_duration == "No heatwave":
            scenario += heatwave_durations[heatwave_duration][1]
        else:
            scenario += heatwave_durations[heatwave_duration]

    scenario += location_types[location_type]

    return scenario


def streamlit_app():
    # Use Streamlit to create the UI components and logic
    st.title("Heatscore")
    st.markdown("""
        ## Heatwave Risk Assessment for the UK
        Assess the potential impact of heatwaves on building occupants across the UK. 
        Select your parameters below to evaluate the risk level. 
        """)

    # Use Streamlit to create selection boxes for each category
    building_type = st.selectbox("Choose Building Type", options=list(building_types.keys()))
    location_type = st.selectbox("Choose Location", options=list(location_types.keys()))
    heatwave_duration = st.selectbox("Choose Heatwave Duration", options=list(heatwave_durations.keys()))
    year = st.selectbox("Choose Year", options=list(years.keys()))

    file = pd.read_excel(file_path, header=1, index_col=2).iloc[:,2:]

    scenario = create_scenario(location_type, heatwave_duration, year)
    archetype = building_types[building_type]
    score = file.loc[scenario, archetype]

    st.metric(label="Risk Level", value=score, delta=None)

    # Convert score to a progress bar with contextual color coding
    progress_value = score / 10
    st.progress(progress_value)

    # Contextual message about the risk level
    if score < 7:
        st.success("Risk is within acceptable limits.")
    elif score < 10:
        st.warning("High risk! Immediate attention required.")
    else:
        st.error("Critical risk level! Take action now.")

        # Add spacing and structure to the additional information section
    st.markdown("---")
    st.markdown("""
       #### Additional Information
       The heat assessment is based on building simulations using the methodology presented in the Heatalyzer paper linked below. The scoring is determined by the maximum Degree hours over some week in the most resilient zone of the building, with a value of at least 120 resulting in a risk level of 10, indicating unlivable conditions. This is in line with the SET Degree hours threshold used in LEED's passive survivability pilot.
       - Heatalyzer paper for the methodology here (*Link to be added*)
       - Code for the tool is available on the Heatalyzer [GitHub](https://github.com/lcapol/Heatalyzer).
       - [LEED's passive survivability pilot](https://www.usgbc.org/credits/passivesurvivability)

       It is essential to prepare now for these risks. The [Solace](https://sites.google.com/view/ucsolace/) project aims to create a global suite of location-specific solutions encompassing both technical and non-technical aspects. Information on existing solutions for buildings is included on the website.
       """)

if __name__ == "__main__":
    streamlit_app()
