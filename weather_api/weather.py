import requests
import time

from MySQLClient import MySQLDatabase
from decouple import config

API_KEY = config('APIKEY')

URL = "http://api.weatherapi.com/v1/forecast.json?key=" + API_KEY + "&q=Montréal";

response = requests.get(URL)
dictDataCurrent = response.json()["current"]
dictDataForecast = response.json()["forecast"]["forecastday"][0]["hour"]

forecastMorning = dictDataForecast[11] # 10am
forecastAfternoon = dictDataForecast[16] # 3pm
forecastNight = dictDataForecast[22] # 9pm

ts = round(time.time())

db = MySQLDatabase(host="localhost", user="username", password="password", database="weather")
db.connect()

record = (str(dictDataCurrent["last_updated"]), str(round(dictDataCurrent["temp_c"])), str(ts), dictDataCurrent["condition"]["text"], str(round(dictDataCurrent["wind_kph"])), str(round(dictDataCurrent["feelslike_c"])))

query_current_weather = """INSERT INTO current_weather (last_updated, temp, time, weather_condition, wind, feelslike) 
VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" % record

record_forecast = (dictDataCurrent["last_updated"], forecastMorning["temp_c"], forecastMorning["wind_kph"], forecastMorning["condition"]["text"], forecastAfternoon["temp_c"], forecastAfternoon["wind_kph"], forecastAfternoon["condition"]["text"], forecastNight["temp_c"], forecastNight["wind_kph"], forecastNight["condition"]["text"])

query_forecast_weather = """INSERT INTO forecast_weather 
(time, 
morning_temp, morning_wind, morning_weather_condition, 
afternoon_temp, afternoon_wind, afternoon_weather_condition, 
night_temp, night_wind, night_weather_condition)
VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % record_forecast

db.execute_query(query_current_weather)

db.execute_query(query_forecast_weather)

db.disconnect()

