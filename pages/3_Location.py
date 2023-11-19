import streamlit as st
import requests
import time
import pydeck as pdk
import db
import folium
import pandas



def get_current_location(api_key):
    try:
        # Make a request to the Google Maps Geolocation API
        response = requests.post(
            f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}',
            json={}
        )

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Check if the response contains location information
            if 'location' in data:
                location = data['location']
                #accuracy = data['accuracy']
                #print('location',location)
                print(f"Latitude: {location['lat']}")
                print(f"Longitude: {location['lng']}")
                #print(f"Accuracy: {accuracy} meters")
                return location
            else:
                print(f"Error: Location information not found in the response.")
                return

        else:
            print(f"Error: Request failed with status code {response.status_code}")
            print(response.text)  # Print the response content for further analysis
        # Sleep for 50 minutes
        time.sleep(3000)
    except Exception as e:
        print(f"Error: {e}")

def get_walmart_locations(api_key, latitude, longitude, radius=3000):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "name": "Walmart",
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    results = response.json().get("results", [])
    return results


def main():
    
    if __name__ == "__main__":
        # Replace 'YOUR_API_KEY' with your actual Google Maps API key
        api_key = 'AIzaSyCln0P5vH9q7oQsZ7CpO4W_BAjTuaLdIn0'
        curLocation = {}
        if api_key == 'YOUR_API_KEY':
            print("Please replace 'YOUR_API_KEY' with your actual Google Maps API key.")
        else:
            curLocation =get_current_location(api_key)
        st.title("Find Location")
            # Set default location (for example, San Francisco)
        latitude = curLocation['lat']
        longitude = curLocation['lng']

        if st.button("Show Walmart Locations"):
            walmart_locations = get_walmart_locations(api_key, latitude, longitude)

            if walmart_locations:
                map_data = [{"latitude": location["geometry"]["location"]["lat"],
                            "longitude": location["geometry"]["location"]["lng"],
                            "tooltip": location["name"],
                            "popup": f"<b>{location['name']}</b><br>{location.get('vicinity', '')}"} for location in walmart_locations]

                st.map(map_data, zoom=12)
            else:
                st.warning("No Walmart locations found.")
        if st.button("Show Insights"):
            st.write('somebody purchased SALONPAS for 13.99 on 11/18/2023')
            st.write('somebody purchased IBERIA GUAV for 0.99 on 11/19/2023')


if "user" not in st.experimental_get_query_params():
    st.experimental_set_query_params(user="no")
if st.experimental_get_query_params()["user"][0] == "no":
    st.title("Login to see this page")
else:
    main()






