import os
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.place_info_search import GooglePlacesSearch

class PlacesSearch:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.getenv("GPLACES_API_KEY")
        self.google_places_search = GooglePlacesSearch(self.google_api_key)
        self.places_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = self.google_places_search.google_search_attractions(place)
                if attraction_result:
                    return f"The attractions of {place} suggested by Google are as follows: {attraction_result}"
                else:
                    return f"Google could not find any attractions of {place}"
            except Exception as e:
                return f"Google cannot find the attractions due to {e}"
            
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurant_result = self.google_places_search.google_search_restaurants(place)
                if restaurant_result:
                    return f"The restaurants of {place} suggested by Google are as follows: {restaurant_result}"
                else:
                    return f"Google could not find any restaurants of {place}"
            except Exception as e:
                return f"Google cannot find the restaurants due to {e}"
            
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activity_result = self.google_places_search.google_search_activities(place)
                if activity_result:
                    return f"The activities of {place} suggested by Google are as follows: {activity_result}"
                else:
                    return f"Google could not find any activities of {place}"
            except Exception as e:
                return f"Google cannot find the activities due to {e}"
            
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transportation_result = self.google_places_search.google_search_transportation(place)
                if transportation_result:
                    return f"The modes of transportation in {place} suggested by Google are as follows: {transportation_result}"
                else:
                    return f"Google could not find any modes of transportation in {place}"
            except Exception as e:
                return f"Google cannot find the modes of transportation due to {e}"
            
        return [search_attractions, search_restaurants, search_activities, search_transportation]