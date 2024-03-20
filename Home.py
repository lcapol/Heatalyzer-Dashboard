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

zones = ['Kitchen and living area', 'Bedroom area']

#SET Degree hours input
file_path_dh = 'data/SET_Max_dh.xlsx'
file_path_new_score = 'data/activity_hours_outputs.xlsx'


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
    st.title("Heatalyzer Dashboard")
    st.markdown("""
        ## Liveability during Heatwaves in London
        Assess the impact of heatwaves on the liveability of residents in London. 
        Select your parameters below to evaluate the risk. 
        """)

    # Use Streamlit to create selection boxes for each category
    building_type = st.selectbox("Choose Building Type", options=list(building_types.keys()))
    zone = st.selectbox("Choose Building Zone", options=zones)
    location_type = st.selectbox("Choose Location", options=list(location_types.keys()))
    heatwave_duration = st.selectbox("Choose Heatwave Duration", options=list(heatwave_durations.keys()))
    year = st.selectbox("Choose Year", options=list(years.keys()))


    if zone == 'Kitchen and living area':
        zone_end = "_KL"
    else:
        zone_end = "_BD"


    # Read in the files
    # Degree hours and degree hours score
    scenario = create_scenario(location_type, heatwave_duration, year)
    archetype = building_types[building_type]

    dh = pd.read_excel(file_path_dh, header=1, index_col=2, sheet_name='Dh' + zone_end).iloc[:, 2:].loc[scenario, archetype]

    hours_mv_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_MV' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_la_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_LA' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_nl_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_NL' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_ns_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_NS' + zone_end).iloc[:, 1:].loc[scenario, archetype]

    hours_mv_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_MV' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_la_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_LA' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_nl_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_NL' + zone_end).iloc[:, 1:].loc[scenario, archetype]
    hours_ns_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_NS' + zone_end).iloc[:, 1:].loc[scenario, archetype]


    st.markdown("---")

    st.markdown("#### LEED's Passive Survivability")

    st.markdown(f"{dh} SET hours")

    st.markdown("---")

    st.markdown("#### Activity Hours")

    data = {
        "Activity": ["Moderate to vigorous activities", "Light activities", "Not liveable", "Not survivable"],
        "Young (18-40 years)": [hours_mv_y, hours_la_y, hours_nl_y, hours_ns_y],
        "Elderly (over 65 years)": [hours_mv_el, hours_la_el, hours_nl_el, hours_ns_el],
    }

    df = pd.DataFrame(data)
    st.dataframe(df.set_index(df.columns[0]), use_container_width=True)



if __name__ == "__main__":
    streamlit_app()
