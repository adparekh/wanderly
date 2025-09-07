import os
from utils.weather_service import WeatherForecast
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

class WeatherInfo:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.weather_service = WeatherForecast(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                cur_temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {cur_temp}°C, {desc}"
            return f"Could not fetch current weather for {city}"
            
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            forecast_data = self.weather_service.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_day = f"{date}: {temp}°C, {desc}"
                    forecast_summary.append(forecast_day)
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch weather forecast for {city}"
        
        return [get_current_weather, get_weather_forecast]