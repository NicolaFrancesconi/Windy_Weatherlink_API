import conversion_function as convf

###################################
# START API KEYS AND SECRETS
###################################
WEATHERLINK_API_KEY = "ovt4dcaqkijquwt5fzfomoyhwq0ltwze" 
WEATHERLINK_API_SECRET = "tonrh7bvimqxcjl7tma2urpv41dbk5tx"
WINDY_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaSI6MTQ1NDg3MDcsImlhdCI6MTc0ODI1MzQ2MX0.AJphOGKvDDHQ_HFYQXJu9N2cm23QOIp86xN321rEpxA"
POST_ON_WINDY_EVERY_N_MINUTES = 16  # Post data on Windy every N minutes; default value 16 minutes
###################################
# END API KEYS AND SECRETS
###################################

###################################
# START STATION PARAMETERS WINDY
###################################
STATION = 0 # Station ID; required for multiple stations; default value 0
STATION_NAME = "Francesconi Davis Station"  # User selected station name
ELEVATION = 21  # Elevation in meters
LATITUDE = 44.27801  # Latitude in decimal degrees
LONGITUDE = 11.95397  # Longitude in decimal degrees
SHARE_OPTION = "Open"  # Share option: Open, Only Windy, Private
TEMPHEIGHT = 8  # Temperature sensor height above the surface in meters
WINDHEIGHT = 10  # Wind sensor height above the surface in meters
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
