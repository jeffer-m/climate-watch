import requests
import os
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()

# Initialize geocoder
geolocator = Nominatim(user_agent="climate_watch_app")

def get_coordinates(location_name):
    """Convert location name to latitude and longitude"""
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def get_weather_data(lat=None, lon=None):
    """Get current weather data for coordinates"""
    # Default to Harare if no coordinates provided
    if lat is None or lon is None:
        lat = -17.83
        lon = 31.05
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,precipitation,weather_code",
        "hourly": "temperature_2m,relative_humidity_2m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Enhanced weather data processing
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        
        return {
            "current": current,
            "hourly": hourly,
            "daily": daily,
            "coordinates": {"latitude": lat, "longitude": lon}
        }
    except Exception as e:
        print("Error fetching weather:", e)
        return {}

def get_climate_data(lat=None, lon=None):
    """Get climate data for coordinates"""
    # Default to Harare if no coordinates provided
    if lat is None or lon is None:
        lat = -17.83
        lon = 31.05
    
    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "1990-01-01",
        "end_date": "2020-12-31",
        "models": "CMCC_CM2_VHR4",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "daily" not in data:
            print("API Response:", data)
            return {}
            
        daily_data = data["daily"]
        years = list(range(1990, 2021))
        
        return {
            "trend_years": years,
            "trend_values": daily_data.get("temperature_2m_max", []),
            "min_temps": daily_data.get("temperature_2m_min", []),
            "rainfall": daily_data.get("precipitation_sum", []),
            "coordinates": {"latitude": lat, "longitude": lon}
        }
    except Exception as e:
        print(f"Climate API Error: {e}")
        return {}

    #ROUTES FOR GETTING NEWS

def get_climate_news(next_page=None):
    api_key = os.getenv("NEWSDATA_API_KEY")
    base_url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=climate&category=environment&language=en"

    if next_page:
        base_url += f"&page={next_page}"

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', []), data.get('nextPage', None)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return [], None



def get_climate_news_bulk(pages=5):
    all_articles = []
    for page in range(1, pages + 1):
        articles = get_climate_news(next_page=page)
        if not articles:
            break  # stop if no more articles available
        all_articles.extend(articles)
    return all_articles

          
