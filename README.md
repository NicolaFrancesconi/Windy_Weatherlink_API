# 🌤️ Weatherlink to Windy Uploader

This Python script periodically fetches weather data from a [Weatherlink](https://www.weatherlink.com/) station and uploads it to [Windy.com](https://stations.windy.com/). It's designed to run continuously and post data at regular intervals.

---

## 🚀 Features

- Automatically fetches live data from your **Weatherlink** station.
- Converts and maps the data to **Windy’s** public API format.
- Posts data at user-defined intervals (aligned with clock intervals).
- Simple setup with API keys and configuration via a `params.py` file.

---

## 🛠️ Requirements

- Python 3.7+
- Required Python packages:

```
requests
schedule
```

---

## 📁 File Structure

```
your_project/
├── WeatherlinkWindy.py         # Your main script
├── params.py                   # Contains API keys and config
└── conversion_function.py      # Contains unit conversion utilities
```

---

## ⚙️ Configuration (`params.py`)

You need to modify the `params.py` file with the following variables:

```python
###################################
# START API KEYS AND SECRETS
###################################
WEATHERLINK_API_KEY = "your_weatherlink_api_key"
WEATHERLINK_API_SECRET = "your_weatherlink_api_secret"
WINDY_API_KEY = "your_windy_api_key"
POST_ON_WINDY_EVERY_N_MINUTES = 16  # Post data on Windy every N minutes; default value 16 minutes
###################################
# END API KEYS AND SECRETS
###################################

###################################
# START STATION PARAMETERS WINDY
###################################
STATION = 0 # Station ID; required for multiple stations; default value 0
STATION_NAME = "Yoir Station Name"  # User selected station name
ELEVATION = XXX  # Elevation in meters
LATITUDE = XXX  # Latitude in decimal degrees of your station
LONGITUDE = XXX  # Longitude in decimal degrees of your station
SHARE_OPTION = "Open"  # Share option: Open, Only Windy, Private
TEMPHEIGHT = XXX  # Temperature sensor height above the surface in meters
WINDHEIGHT = XXX  # Wind sensor height above the surface in meters
###################################
# END STATION PARAMETERS WINDY
###################################

###################################
# START PARAMETERS MAPPING WEATHER-WINDY
###################################
FIELD_MAPPING = {
            "hum" : ("rh", convf.identity), # Relative Humidity in percentage
            "dew_point" : ("dew_point", convf.identity), # Dew Point in Celsius
            "uv_index" : ("uv", convf.identity), # UV Index
            "wind_speed_last" : ("wind", convf.identity), # Wind Speed in m/s
            "wind_dir_last" : ("winddir", convf.identity), # Wind Direction in degrees
            "wind_speed_hi_last_2_min" : ("windgust", convf.identity), # Wind Gust in m/s
            "rainfall_last_60_min_mm" : ("precip", convf.identity), # Precipitation in mm over the last 60 minutes
            "bar_sea_level" : ("mbar", convf.inchesOfMercury_to_mbar), # Pressure from inches of mercury to millibar (hPa)
            "temp" : ("temp", convf.fahrenheit_to_celsius), # Temperature from Fahrenheit to Celsius
        }
###################################
# END PARAMETERS MAPPING WEATHER-WINDY
###################################

```

---

## 🏃‍♂️ How to Run

Once everything is configured in the cmd go to the folder of the script and run:

```bash
python WeatherlinkWindy.py
```

The script will:
- Wait until the next aligned interval (e.g., 10:00, 10:15, etc.)
- Fetch the data and post it
- Continue doing so every `POST_ON_WINDY_EVERY_N_MINUTES` minutes

You’ll see logs for each fetch and post cycle.

---

## 🧪 Sample Output

```
Weather upload service started. Press Ctrl+C to stop.
Waiting for the next interval. Sleeping for 245 seconds.
Weather Data:
Temperature: 19.5 °C
Relative Humidity: 75 %
Dew Point: 14.3 °C
UV Index: 2
Wind Speed: 4.5 m/s
...
[SUCCESS] Data posted successfully to Windy.
```

---

## Error Handling

- Gracefully handles API request failures.
- Catches unexpected exceptions and logs them.
- Can be safely stopped with `Ctrl+C`.

---

