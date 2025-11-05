import time
def fetch_data():
    """Simulates API call"""
    current_time = time.strftime('%B, %d - %Y', time.localtime())
    return {
        "temperature_c": 25,
        "weather": "Cloudy",
        "time":  current_time
    }

#print(fetch_data()["time"])