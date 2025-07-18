import requests
import params
import conversion_function as convf
from datetime import datetime, timedelta
import schedule
import time

class WeatherlinkWindy:
    """
    A class to fetch weather data from Weatherlink and publish it to Windy.
    """
    def __init__(self) -> None:
        self.weatherlink_api_key = params.WEATHERLINK_API_KEY
        self.weatherlink_api_secret = params.WEATHERLINK_API_SECRET
        self.weatherlink_station_id = self.get_weatherlink_station_id()
        
        self.windy_api_key = params.WINDY_API_KEY
        self.windy_station_id = params.STATION
        self.station_name = params.STATION_NAME
        self.elevation = params.ELEVATION
        self.latitude = params.LATITUDE
        self.longitude = params.LONGITUDE
        self.share_option = params.SHARE_OPTION
        self.tempheight = params.TEMPHEIGHT
        self.windheight = params.WINDHEIGHT
        self.field_mapping = params.FIELD_MAPPING
        
        self.station_dict = {
                "station": self.windy_station_id,
                "name": self.station_name,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "elevation": self.elevation,
                "tempheight": self.tempheight,
                "windheight": self.windheight,
                "shareOption": self.share_option
            }
        
    def fetch_and_post_weather_data(self, Verbose=True):
        """Fetches weather data from Weatherlink and posts it to Windy."""
        weather_data = self.get_weatherlink_data()
        json_data = self.get_json_to_post(weather_data, Verbose)
        self.post_data_on_windy(json_data)
        
    def get_weatherlink_station_id(self):
        """
        Fetches the station ID from Weatherlink API.
        Returns the station ID if found, otherwise returns None.
        """
        weatherlink_url = f"https://api.weatherlink.com/v2/stations?api-key={self.weatherlink_api_key}"
        headers = {"X-Api-Secret": self.weatherlink_api_secret}
        
        try:
            response = requests.get(weatherlink_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            stations = response.json().get("stations", [])
            if stations:
                return stations[0].get("station_id")
            else:
                return None
        except requests.RequestException as e:
            print(f"Error fetching station ID: {e}")
            return None
        
    def get_weatherlink_data(self):
        """
        Fetches current weather data from Weatherlink API.
        Returns the data if successful, otherwise returns None.
        """
        weatherlink_url = f"https://api.weatherlink.com/v2/current/{self.weatherlink_station_id}?api-key={self.weatherlink_api_key}"
        headers = {"X-Api-Secret": self.weatherlink_api_secret}
        try:
            response = requests.get(weatherlink_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        
    def post_data_on_windy(self, data):
        windy_url = f"https://stations.windy.com/pws/update/{self.windy_api_key}"
        headers = {"Content-Type": "application/json"}
        
        #print("Data to post on Windy:", data)

        try:
            response = requests.post(windy_url, headers=headers, json=data, timeout=10)
            # Check HTTP status
            if response.status_code != 200:
                print(f"[ERROR] HTTP {response.status_code}: {response.reason}")
                return False

            # Try to parse the response JSON
            response_json = response.json()

            # Check if there are any errors in the response
            errors = response_json.get("update", {}).get("errors", {})
            if errors.get("stations") or errors.get("observations"):
                print("[ERROR] Windy API reported errors:")
                print(errors)
                return False

            # Check for success confirmation
            result = response_json.get("result", {})
            for station_id, result_data in result.items():
                station_success = all(entry.get("success", False) for entry in result_data.get("stations", []))
                obs_success = all(entry.get("success", False) for entry in result_data.get("observations", []))
                if not (station_success and obs_success):
                    #print(f"[ERROR] Station or observation update failed for station {station_id}")
                    # PRINT THE ERROR DETAILS
                    for obs in result_data.get("observations", []):
                        if not obs.get("success") and "error" in obs:
                            print("[ERROR]", obs["error"])
                    return False

            print("[SUCCESS] Data posted successfully to Windy.")
            return True

        except requests.exceptions.RequestException as e:
            print(f"[EXCEPTION] Request failed: {e}")
            return False
        except ValueError:
            print("[EXCEPTION] Failed to decode JSON response.")
            return False
        
    def get_json_to_post(self, weather_data, verbose=True):
        """
        Prepares the JSON file with the required structure.
        Returns the JSON string.
        """
        observation_dict = {
            "station": self.windy_station_id
        }
        timestamp = None  # Initialize timestamp variable
        tz_offset = None  # Initialize timezone offset variable
        for sensor in weather_data["sensors"]:
            sensor_data = sensor["data"][0]  # Get the first data entry
            # Extract timestamp and timezone offset
            if timestamp is None or tz_offset is None:
                timestamp = sensor_data.get("ts")
                tz_offset = 0
                observation_dict["time"] = convf.timestamp_to_iso(timestamp, tz_offset)
            
            for weatherlink_key, (windy_key, convert ) in self.field_mapping.items():
                value = sensor_data.get(weatherlink_key)
                if value is not None:
                    observation_dict[windy_key] = convert(value)
        data = {
            "stations": [self.station_dict],
            "observations": [observation_dict]
        }
        
        
        if verbose:
            self.print_observation_data(observation_dict)
        
        
        return data
        
    def print_observation_data(self, observation_dict):
        """
        Prints the weather data in a readable format.
        """
        print("Weather Data:")
        print(f"Temperature: {observation_dict['temp']} °C")
        print(f"Relative Humidity: {observation_dict['rh']} %")
        print(f"Dew Point: {observation_dict['dew_point']} °C")
        print(f"UV Index: {observation_dict['uv']} ")
        print(f"Wind Speed: {observation_dict['wind']} m/s")
        print(f"Wind Direction: {observation_dict['winddir']} degrees")
        print(f"Wind Gust: {observation_dict['windgust']} m/s")
        print(f"Precipitation (last 60 min): {observation_dict['precip']} mm")
        print(f"Pressure (mbar): {observation_dict['mbar']} mbar")
        print(f"Time: {observation_dict['time']}")   

    def seconds_to_next_interval(self,interval_minutes):
        """
        Calculates the number of seconds until the next time interval.

        Parameters:
            interval_minutes (int): The interval in minutes.

        Returns:
            float: Seconds until the next interval aligned with the hour.
        """
        now = datetime.now()
        total_minutes = now.hour * 60 + now.minute
        next_interval = ((total_minutes // interval_minutes) + 1) * interval_minutes

        next_hour = (next_interval // 60) % 24  # Wrap around if past 24h
        next_minute = next_interval % 60
        days_to_add = (total_minutes + interval_minutes) // (24 * 60)  # Handle day rollover
        next_time = now.replace(hour=next_hour, minute=next_minute, second=0, microsecond=0) + timedelta(days=days_to_add)
        return (next_time - now).total_seconds()
        



if __name__ == "__main__":
    print("Weather upload service started. Press Ctrl+C to stop.")
    first_post = True  # Flag to indicate the first run
    api_interface = WeatherlinkWindy()
    while True:
        try:
            if first_post:
                delay_seconds = api_interface.seconds_to_next_interval(params.POST_ON_WINDY_EVERY_N_MINUTES)  # Calculate seconds to the next 15-minute interval
                print(f"Waiting for the next interval. Sleeping for {int(delay_seconds)} seconds.")
                time.sleep(delay_seconds)
                api_interface.fetch_and_post_weather_data()  # Initial fetch and post
                schedule.every(params.POST_ON_WINDY_EVERY_N_MINUTES).minutes.do(api_interface.fetch_and_post_weather_data)
                first_post = False                    
            else:
                schedule.run_pending()
                time.sleep(1)
            
        except KeyboardInterrupt:
            print("Stopping the Weather upload service.")
            break
        
        except Exception as e:
            print(f"An error occurred: {e}")