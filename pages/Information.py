import streamlit as st


def information_page():

    st.title("Information")

    st.markdown("### Selection Options")

    st.markdown("#### Building Types")

    st.markdown("""The selection of building types is based on the [CODE](https://assets.publishing.service.gov.uk/media/632038fee90e077dba7762a6/CODE-Final-Report-WHOLE-FINAL-v20.pdf) study of the UK housing stock by the UK Department for Business, 
    Energy & Industrial Strategy (BEIS), which defines archetypes representing 88% of Britain's dwellings. 
    These archetypes are based on the most common combinations of dwelling types (flats, terraced houses, bungalows, semi-detached, and detached houses) 
    and construction forms (cavity or solid walls, and solid or suspended timber floors). 
    The Heatscore provides results for these building types by allowing the selection of 8 archetypes representing the majority of the housing stock.
    """)
    st.markdown("""
    Descriptions of the 8 provided housing types:
    - **Ground Floor Flats**: Ground floor flats.
    - **Mid Floor Flats**: Intermediate floor flats.
    - **Top Floor Flats**: Top floor flats with roof.
    - **Bungalow houses**: Single-storey homes, any dwelling other than a flat with a ground floor but no first floor.
    - **Mid-terraced houses (non-bungalow) with cavity walls (post-1945)**: Terraced homes with two shared walls and at least two floors (not a bungalow). This construction has cavity walls and solid floors,
    typically found in newer houses built post-1945. 
    - **Mid-terraced houses (non-bungalow) with solid walls (pre-1945)**: Terraced homes with two shared walls and at least two floors (not a bungalow). This construction has solid walls and suspended floors,
    typically found in older houses built pre-1945. 
    - **End-terraced, Semi-detached, detached houses (non-bungalow) with cavity walls (post-1945)**: Representing end-terraced, semi-detached, or detached houses, with at least two floors (not a bungalow). This construction has cavity walls and solid floors,
    typically found in newer houses built post-1945. 
    - **End-terraced, Semi-detached, detached houses (non-bungalow) with solid walls (pre-1945)**: Representing end-terraced, semi-detached, or detached houses, with at least two floors (not a bungalow). This construction has solid walls and suspended floors,
    typically found in older houses built pre-1945. 
    """)


    st.markdown("#### Location")

    st.markdown("""The location selection is based on ranges of urban heat island (UHI) effect intensities. 
    Three options are given depending on the location of the dwelling within the urban environment. Hereby, the UHI intensity represents the value by which the hourly temperature values are 
    expected to be higher on average over the summer months compared to rural surroundings. 
     """)
    st.markdown("""
    Options for the UHI intensity include:
    - **Greenery nearby (0 °C UHI)**
    - **Some greenery nearby (1 °C UHI)**
    - **Areas with no greenery nearby (2 °C UHI)**
    """)

    st.markdown("#### Heatwave Duration")

    st.markdown("""Heatwave duration is categorized based on the length of consecutive hot days, ranging from no heatwave to heatwaves with the peak condition lasting 1, 3, 5, or 7 days. 
    The duration hereby represents the length of the hottest day of the heatwave. This allows assessing the resilience of buildings and their occupants to varying lengths of extreme heat conditions.
    """)

    st.markdown("""
    Options for the heatwave duration include:
    - **No heatwave:** Typical weather conditions for the climate during the specified year. 
    - **1 day heatwave:** Heatwave scenario for the specified year. 
    - **3 days heatwave:** Heatwave scenario for the specified year where the peak day lasts 3 days. 
    - **5 days heatwave:** Heatwave scenario for the specified year where the peak day lasts 5 days. 
    - **7 days heatwave:** Heatwave scenario for the specified year where the peak day lasts 7 days. 
    """)

    st.markdown("#### Year")

    st.markdown("""The year selection allows for the examination of heatwave impacts under current conditions and future climate projections for 2030, 2050, and 2080. 
    This allows an understanding of how changing climate conditions may influence the risk levels associated with heatwaves in UK dwellings.
    """)

    st.markdown("""
    Options for the year include:
    - **Current:** Weather scenarios for the current climate conditions.
    - **2030:** Weather scenarios for projected future climate conditions in 2030 according to RCP4.5 sceanrio. 
    - **2050:** Weather scenarios for projected future conditions in 2050 according to RCP4.5 sceanrio. 
    - **2080:** Weather scenarios for projected future climate conditions in 2080 according to RCP4.5 sceanrio. 
    """)
    st.markdown("---")


    st.markdown("### Methodologies for Risk Level Assessment")
    st.markdown("""
    To assess the potential impact of heatwaves on building occupants, three risk assessments are reported based on two methodologies. The approaches used are based on livability limits for SET Degree hours as described in LEED's passive survivability pilot ([here](https://www.usgbc.org/credits/passivesurvivability)) and evaluation of the number of hours of different possible activity levels for two age groups (18-45 years and over 65 years) based on more recent work ([here](https://www.nature.com/articles/s41467-023-43121-5)). 
    The goal is to offer insights into the thermal comfort and potential health risks occupants face during extreme heat events. 

    **1. SET Degree hours:**
    This approach calculates the highest Standard Effective Temperature (SET) Degree hours observed over some week. The assessment follows LEED's passive survivability pilot, which employs a temperature threshold of 30 degrees Celsius. Note that 120 SET Degree hours (Dh) over one week is considered as the liveability limit. 
    We are reporting the Dh of the most resilient housing zone.

    **2. Activity hours:**
    Using the liveability ranges described in the Heatalyzer paper, this assessment counts the number of hours over the hottest summer week that occupants can perform moderate to vigorous physical activities (3.0 or more METs),
    where only light physical activities (1.5-3.0 METs) are possible, and the number of hours that are not liveable and not survivable anymore. This calculation is performed separately for young (18-45 years) and elderly (over 65 years) occupants.
    """)
    # , to align with standards that suggest no more than 3-5% of occupied hours should exceed comfort limits.

    st.markdown("---")

    st.markdown("### Links")
    st.markdown("""
       The score values are based on building simulations using the methodology presented in the Heatalyzer paper linked below. Links are provided
       for the Heatalyzer tool, allowing this evaluation for further building and weather scenarios of interest, and other relevant background information.
       - Heatalyzer paper on the methodology [here](https://www.cambridge.org/engage/coe/article-details/65ccc858e9ebbb4db958f3e9)
       - Code for the tool is available on the Heatalyzer [GitHub](https://github.com/lcapol/Heatalyzer).
       - [LEED's passive survivability pilot](https://www.usgbc.org/credits/passivesurvivability)
       - Cost-Optimal Domestic Electrification (CODE) study report by the UK Department of Business, Energy & Industrial Strategy (BEIS) [here](https://assets.publishing.service.gov.uk/media/632038fee90e077dba7762a6/CODE-Final-Report-WHOLE-FINAL-v20.pdf)
     
       It is essential to prepare now for these risks. The following [website](https://www.transitioncambridge.org/wiki/TTEnergy/HowToKeepCool) "How to keep cool in summer" contains information on strategies to employ.
       """)


if __name__ == "__main__":
    information_page()