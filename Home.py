import streamlit as st
import pandas as pd
from st_aggrid import AgGrid


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
file_path_new_score = 'data/score_vector_outputs.xlsx'


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
        ## Heatwave Risk Assessment for London
        Assess the potential impact of heatwaves on building occupants in London. 
        Select your parameters below to evaluate the risk level. 
        """)

    # Use Streamlit to create selection boxes for each category
    building_type = st.selectbox("Choose Building Type", options=list(building_types.keys()))
    location_type = st.selectbox("Choose Location", options=list(location_types.keys()))
    heatwave_duration = st.selectbox("Choose Heatwave Duration", options=list(heatwave_durations.keys()))
    year = st.selectbox("Choose Year", options=list(years.keys()))

    # Read in the files
    # Degree hours and degree hours score
    file_dh = pd.read_excel(file_path_dh, header=1, index_col=2, sheet_name='Degree Hours').iloc[:, 2:]
    file_dh_score = pd.read_excel(file_path_dh, header=1, index_col=2, sheet_name='Clipped Scoring').iloc[:, 2:]
    #Risk score elderly
    file_ns_el_kl = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Score_Elderly_KL').iloc[:, 1:]
    file_ns_el_bd = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Score_Elderly_BD').iloc[:, 1:]
    #Risk score young
    file_ns_y_kl = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Score_Young_KL').iloc[:, 1:]
    file_ns_y_bd = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Score_Young_BD').iloc[:, 1:]

    scenario = create_scenario(location_type, heatwave_duration, year)
    archetype = building_types[building_type]
    score_dh = file_dh_score.loc[scenario, archetype]
    dh = file_dh.loc[scenario, archetype]
    score_ns_el_kl = file_ns_el_kl.loc[scenario, archetype]
    score_ns_el_bd = file_ns_el_bd.loc[scenario, archetype]
    score_ns_y_kl = file_ns_y_kl.loc[scenario, archetype]
    score_ns_y_bd = file_ns_y_bd.loc[scenario, archetype]

    #extract number of hours of different activities possible for less affected zone
    if score_ns_el_kl < score_ns_el_bd:
        el_zone = "_KL"
        score_ns_el = score_ns_el_kl
    else:
        el_zone= "_BD"
        score_ns_el = score_ns_el_bd

    if score_ns_y_kl < score_ns_y_bd:
        y_zone = "_KL"
        score_ns_y = score_ns_y_kl
    else:
        y_zone= "_BD"
        score_ns_y = score_ns_y_bd

    hours_mv_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_MV' + el_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_la_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_LA' + el_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_nl_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_NL' + el_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_ns_el = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Elderly_NS' + el_zone).iloc[:, 1:].loc[scenario, archetype]

    hours_mv_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_MV' + y_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_la_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_LA' + y_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_nl_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_NL' + y_zone).iloc[:, 1:].loc[scenario, archetype]
    hours_ns_y = pd.read_excel(file_path_new_score, header=1, index_col=1, sheet_name='Young_NS' + y_zone).iloc[:, 1:].loc[scenario, archetype]

    #st.metric(label="Risk Level SET Degree hours", value=score_dh, delta=None)

    #progress_value = score_dh / 10
    #st.progress(progress_value)

    #Contextual message about the risk level
    #if score_dh < 7:
    #    st.success("Low to moderate risk.")
    #elif score_dh < 10:
    #    st.warning("Significant risk.")
    #else:
    #   st.error("Critical risk.")
    st.markdown("---")

    st.markdown("#### LEED's Passive Survivability")

    st.markdown(f"{dh} Degree hours")

    st.markdown("---")

    st.markdown("#### Activity Hours")

    data = {
        "Activity": ["Moderate to vigorous activities", "Light activities", "Not liveable", "Not survivable"],
        "Young (18-45 years)": [hours_mv_y, hours_la_y, hours_nl_y, hours_ns_y],
        "Elderly (over 65 years)": [hours_mv_el, hours_la_el, hours_nl_el, hours_ns_el],
    }

    df = pd.DataFrame(data)
    AgGrid(df, fit_columns_on_grid_load=True, theme = 'alpine')


if __name__ == "__main__":
    streamlit_app()
