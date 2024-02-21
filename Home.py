import streamlit as st
import pandas as pd

building_types = {"Ground floor flats": "Ground floor flat",
                 "Mid floor flats": "Mid floor flat",
                  "Top floor flats": "Top floor flat",
                  "Bungalow houses": "Bungalow (detached)",
                  "Mid-terraced houses (non-bungalow) with cavity walls (post-1945)": "Mid terrace (Cavity/solid)",
                  "Mid-terraced houses (non-bungalow) with solid walls (pre-1945)": "Mid terrace (Solid/suspended)",
                  "End-terraced, Semi-detached, detached houses (non-bungalow) with cavity walls (post-1945)": "Compact house (semi-d)",
                  "End-terraced, Semi-detached, detached houses (non-bungalow) with solid walls (pre-1945)": "Medium house, solid (semi-d)"}

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
file_path_dh = 'data/SET_Max_dh_scoring.xlsx'
file_path_new_score = 'data/new_score.xlsx'

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

    file_dh = pd.read_excel(file_path_dh, header=1, index_col=2, sheet_name='Degree Hours').iloc[:,2:]
    file_dh_score = pd.read_excel(file_path_dh, header=1, index_col=2, sheet_name='Clipped Scoring').iloc[:,2:]
    file_ns_el = pd.read_excel(file_path_new_score, header=1, index_col=2, sheet_name='Elderly').iloc[:,2:]
    file_ns_y = pd.read_excel(file_path_new_score, header=1, index_col=2, sheet_name='Young').iloc[:,2:]

    scenario = create_scenario(location_type, heatwave_duration, year)
    archetype = building_types[building_type]
    score_dh = file_dh_score.loc[scenario, archetype]
    dh = file_dh.loc[scenario, archetype]
    h_ns_el = file_ns_el.loc[scenario, archetype]
    h_ns_y = file_ns_y.loc[scenario, archetype]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Risk Level SET Degree hours", value=score_dh, delta=None)

        st.markdown(f"{dh} Degree hours")

        progress_value = score_dh / 10
        st.progress(progress_value)

        #Contextual message about the risk level
        if score_dh < 7:
            st.success("Low to moderate risk.")
        elif score_dh < 10:
            st.warning("Significant risk.")
        else:
           st.error("Critical risk.")

    with col2:
        score_ns_el = min(h_ns_el, 10)
        st.metric(label="Risk Level Elderly (over 65 years)", value=score_ns_el, delta=None)

        st.markdown(f"{h_ns_el} hours")

        progress_value = score_ns_el / 10
        st.progress(progress_value)

        if score_ns_el < 7:
            st.success("Low to moderate risk.")
        elif score_ns_el < 10:
            st.warning("Significant risk.")
        else:
            st.error("Critical risk.")

    with col3:
        score_ns_y = min(h_ns_y, 10)
        st.metric(label="Risk Level Young (18-45 years)", value=score_ns_y, delta=None)

        st.markdown(f"{h_ns_y} hours")

        progress_value = score_ns_y / 10
        st.progress(progress_value)


        if score_ns_y < 7:
            st.success("Low to moderate risk.")
        elif score_ns_y < 10:
            st.warning("Significant risk.")
        else:
            st.error("Critical risk.")



if __name__ == "__main__":
    streamlit_app()
