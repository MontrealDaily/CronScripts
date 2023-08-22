import requests
import time

from MySQLClient import MySQLDatabase
from decouple import config

API_KEY = config('APIKEY')

response = requests.get("http://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=Montréal")
#print(response.json()) # Print response
dictData = response.json()["current"]

ts = round(time.time())

db = MySQLDatabase(host="localhost", user="username", password="password", database="weather")
db.connect()

insert_data_query = "INSERT INTO current_weather (last_updated, temp, time, weather_condition, wind) VALUES ('" + dictData["last_updated"] + "', '" + str(round(dictData["temp_c"])) + "', '" + str(ts) + "', '" + dictData["condition"]["text"] + "', '" + str(round(dictData["wind_kph"])) + "')"
db.execute_query(insert_data_query)

db.disconnect()

