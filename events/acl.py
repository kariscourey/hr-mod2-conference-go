from .keys import PEXEL_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_image(city, state):

    """ Create a dictionary for the headers to use in the request
    Create the URL for the request with the city and state
    Make the request
    Parse the JSON response
    Return a dictionary that contains a `image_url` key and
    one of the URLs for one of the pictures in the response"""

    # identify auth
    headers = {
        'Authorization': PEXEL_API_KEY,
    }

    # make a request to site for data
    res = requests.get(
        f"https://api.pexels.com/v1/search?query={city}+{state}&per_page=1",
        headers=headers,
    )

    # get first image from pexel request
    return res.json()['photos'][0]['src']['original']


def get_weather(city, state):

    """# Create the URL for the geocoding API with the city and state
    # Make the request
    # Parse the JSON response
    # Get the latitude and longitude from the response

    # Create the URL for the current weather API with the latitude
    #   and longitude
    # Make the request
     Parse the JSON response
     Get the main temperature and the weather's description and put
       them in a dictionary
    Return the dictionary"""

    # # identify auth
    # headers = {
    #     'Authorization': OPEN_WEATHER_API_KEY,
    # }

    # make a request to site for data (coorindates)
    res = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state}&limit={1}&appid={OPEN_WEATHER_API_KEY}",
        # headers=headers,
    )

    # get coordinates
    lat = res.json()[0]['lat']
    lon = res.json()[0]['lon']

    # make a request to site for data (weather)
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}",
        # headers=headers,
    )

    # get weather data
    weather = res.json()['weather'][0]

    # adjust weather data with pop (to show only main, desc)
    for i in ['id', 'icon']:
        weather.pop(i)

    # return weather
    return weather
