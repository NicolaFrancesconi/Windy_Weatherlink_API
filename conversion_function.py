from datetime import datetime, timezone

def identity(x):
    """ 
    Returns the input value unchanged.
    """
    return x

def fahrenheit_to_celsius(f):
    """
    Converts Fahrenheit to Celsius.
    """
    return (f - 32) * 5.0 / 9.0 if f is not None else None

def mph_to_mps(mph):
    """
    Converts miles per hour to meters per second.
    """
    return mph * 0.44704 if mph is not None else None

def inches_to_mm(inches):
    """
    Converts inches to millimeters.
    """
    return inches * 25.4 if inches is not None else None

def inchesOfMercury_to_mbar(inHg):
    """
    Converts inches of mercury to millibar (hPa).
    """
    return inHg * 33.8639 if inHg is not None else None

def timestamp_to_iso(ts, tz_offset=0):
    """
    Converts a timestamp to ISO format, adjusting for timezone offset.
    """
    if ts is None:
        return None
    time = datetime.fromtimestamp(ts + tz_offset, tz=timezone.utc)
    return time.isoformat()



