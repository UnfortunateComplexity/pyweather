import requests, json
import datetime, calendar, pytz
from tzlocal import get_localzone
from geopy.geocoders import Nominatim
from geopy import geocoders  
from timezonefinder import TimezoneFinder
from pytz import timezone

#pip mods needed --> nltk, geopy, tzlocal, timezonefinder

from pyfiglet import Figlet


#-------------------------------------------------------------------------------------------------
#Useful functions below:

def kelvToCels(K):
	'''
	Converts an input temperature from Kelvin to Celsius.
	That's it.

	Parameter(s):
	arg1(int): Temperature unit in Kelvin.

	Returns:
	int: Temperature unit converted to Celsius.

	'''
	return (K - 273.15)
# -------------------------------------------------------------------------------------------------

api_key = "07f41ff15e82473ee2aa3733a0efa3d5"								#from openWeatherMap

base_url = "http://api.openweathermap.org/data/2.5/weather?"				#for requesting

print("Hello! Welcome to pyWeather!\n")
#custom_fig = Figlet(font='house_of')
#print(custom_fig.renderText('Hello! Welcome to pyWeather!\n'))


city_name = input("Enter the name of a city to get its weather details : ") 

#Plan to show city timezone details!:
gn = geocoders.GeoNames(username = 'totalbsing')

print("You have chosen to check the weather details of: "   + str(gn.geocode(city_name)))

locator = Nominatim(user_agent='myGeocoder')
location = locator.geocode(city_name)
print("The city is located at Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

tf = TimezoneFinder()
latitude, longitude = location.latitude, location.longitude
cityTZ = tf.timezone_at(lng=longitude, lat=latitude)
print("Timezone: " + cityTZ)

cityTimeAll = datetime.datetime.now(pytz.timezone(cityTZ))
cityTime = cityTimeAll.strftime("%H:%M:%S")

print("It is currently: " + str(cityTime) + " at " + str(city_name))

complete_url = (base_url + "appid=" + api_key + "&q=" + city_name) 

response = requests.get(complete_url) 
x = response.json() 														#format the response to JSON format



if x["cod"] != "404": 

	y = x["main"] 

	currTemp_kelv = y["temp"] 									#currentTemperature
	currTemp_cels = kelvToCels(currTemp_kelv)					#converted to the superior temperature unit
	currTemp_feelsK = y["feels_like"]							# similar as above
	currTemp_feelsC = kelvToCels(currTemp_feelsK)

	current_pressure = y["pressure"] 							#who even checks this?
	current_humidiy = y["humidity"] 							#?

	z = x["weather"] 
	weather_description = z[0]["description"] 

	print(
		"\n Temperature  : " + str(currTemp_kelv) + "K" + 
		"\t / " + str("{:.2f}".format(currTemp_cels)) + "C" +
		"\n Feels like  : " + str(currTemp_feelsK) + "K" + 
		"\t / " + str("{:.2f}".format(currTemp_feelsC)) + "C" +

		"\n Pressure :" + str(current_pressure) + "hPa" +
		"\n Humidity : " + str(current_humidiy) + "%" +
		"\n The description being: " + str(weather_description)
		)

else: 
	print("Sorry, that city either doesnt exist or is not in the database!\n") 


 

# Adapted from:
# https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
# Other references:
# https://stackoverflow.com/questions/62623062/get-time-from-city-name-using-python
# https://stackoverflow.com/questions/13686001/python-module-for-getting-latitude-and-longitude-from-the-name-of-a-us-city
# https://pypi.org/project/timezonefinder/
# https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python
# https://www.geeksforgeeks.org/get-current-time-in-different-timezone-using-python/



# Would you like to know more?