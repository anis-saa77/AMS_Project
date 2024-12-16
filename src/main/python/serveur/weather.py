from datetime import datetime

def check_weather(location: str, at_time: datetime | None = None) -> str:
    '''Return the weather forecast for the specified location.'''
    return f"Il fait toujours beau à {location}"