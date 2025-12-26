import streamlit as st
import requests

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == pwd and user != "":
            st.session_state.login = True
            st.rerun()   
        else:
            st.error("Login failed")

else:
    st.title("Weather Page")

    city = st.text_input("Enter City")

    if st.button("Get Weather"):
        if city != "":
            geo = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            ).json()

            if "results" in geo:
                lat = geo["results"][0]["latitude"]
                lon = geo["results"][0]["longitude"]

                weather = requests.get(
                    f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                ).json()

                w = weather["current_weather"]
                st.write("Temperature:", w["temperature"], "°C")
                st.write("Wind Speed:", w["windspeed"], "km/h")
            else:
                st.error("City not found")
        else:
            st.warning("Enter city name")

    if st.button("Logout"):
        st.session_state.login = False
        st.success("Thanks for using ")
