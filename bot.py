import sys
import json
import requests
from datetime import datetime

# ==========================================
# Project: Autonomous Daily Summary Bot
# Author: Amal M Anand
# ==========================================

# Configuration
CITY = "Thiruvananthapuram"
WTTR_URL = f"https://wttr.in/{CITY}?format=j1"
ZENQUOTES_URL = "https://zenquotes.io/api/random"
SUMMARY_FILE = "daily_summary.md"

def fetch_weather() -> str:
    """Fetches weather data with strict timeout and fallback handling."""
    try:
        response = requests.get(WTTR_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse the specific JSON structure of wttr.in
        current = data['current_condition'][0]
        temp = current['temp_C']
        desc = current['weatherDesc'][0]['value']
        feels_like = current['FeelsLikeC']
        
        return f"🌡️ **{temp}°C** ({desc}) — Feels like {feels_like}°C in {CITY}."
        
    except requests.exceptions.RequestException as e:
        print(f"Weather API Network Error: {e}")
        return "⚠️ Weather data currently unavailable due to network timeout."
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Weather Data Parsing Error: {e}")
        return "⚠️ Weather data format changed or returned invalid structure."

def fetch_quote() -> str:
    """Fetches a random quote with type validation."""
    try:
        response = requests.get(ZENQUOTES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            quote = data[0].get('q', 'No quote found.')
            author = data[0].get('a', 'Unknown')
            return f"> \"{quote}\"\n> \n> — **{author}**"
        return "> ⚠️ Quote format unexpected."
        
    except requests.exceptions.RequestException as e:
        print(f"Quote API Network Error: {e}")
        return "> ⚠️ Inspiration is taking a sick day. Check back tomorrow!"

def generate_summary():
    """Compiles fetched data into a markdown file."""
    date_str = datetime.now().strftime("%A, %B %d, %Y")
    
    print("Executing Weather API Call...")
    weather_text = fetch_weather()
    
    print("Executing ZenQuotes API Call...")
    quote_text = fetch_quote()
    
    summary_content = f"""# Daily Autonomous Summary 🤖

**Date:** {date_str}

## 🌤️ Weather Update
{weather_text}

## 💡 Daily Inspiration
{quote_text}

---
*Generated automatically via GitHub Actions.*
"""
    
    try:
        with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
            file.write(summary_content)
        print(f"Successfully generated {SUMMARY_FILE}")
    except IOError as e:
        print(f"File System Error: Could not write summary file. {e}")
        sys.exit(1) # Force workflow failure if file cannot be written

if __name__ == "__main__":
    generate_summary()
