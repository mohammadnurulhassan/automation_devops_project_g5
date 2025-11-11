import pytest
from weather_app.api_call import f_to_c, transform_weather

#pytestmark = pytest.mark.unit  

def test_f_to_c_rounds_expected():
    assert f_to_c(50.0) == 10.0
    assert f_to_c(41.0) == 5.0

def test_transform_weather_basic_mapping():
    payload = {
        "name": "Stockholm",
        "main": {"temp": 50.0, "feels_like": 46.4, "humidity": 80, "pressure": 1012},
        "weather": [{"description": "light rain", "icon": "10d"}],
        "rain": {"1h": 0.3},
    }
    out = transform_weather(payload)
    assert out["city"] == "Stockholm"
    assert out["description"] == "light rain"
    assert out["temperature_f"] == 50.0
    assert out["feels_like_f"] == 46.4
    assert out["temperature_c"] == 10.0
    assert out["feels_like_c"] == 8.0
    assert out["humidity"] == 80
    assert out["pressure"] == 1012
    assert out["precipitation_mm"] == 0.3
