#!/usr/bin/env python
# coding: utf-8

# In[100]:


import requests
import json
import telebot
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import time
from gpiozero import InputDevice
from time import sleep
from multiprocessing import Process
global is_rain,is_water

from geopy.geocoders import Nominatim
global api_key
api_key = 'b1f9d1f51dbf475d9c4104253233003'
global lat 
lat = 38.040585
lat = str(lat)
global long
long = -84.503716
long = str(long)
complete_url = "https://api.weatherapi.com/v1/forecast.json?key="+api_key+"&q="+lat+","+long+"&days=2&aqi=no&alerts=yes"
response = requests.get(complete_url)
x = response.json()


# In[101]:


def print_weather_condition_by_day(x):
    temp = x['forecast']['forecastday']
    st = ""
    for i in temp:
        st += i['date']
        st += "\n"
        st += "Max Temperature: "+str(i['day']['maxtemp_c'])
        st += "\n"
        st += "Min Temperature: "+str(i['day']['mintemp_c'])
        st += "\n"
        st += 'Weather: '+str(i['day']['condition']['text'])
        st += "\n"
    return st
        


# In[102]:


print_weather_condition_by_day(x)


# In[103]:


def print_if_rain(x):
    temp = x['forecast']['forecastday']
    st = ""
    for i in temp:
        temp1 = i['hour']
        for j in temp1:
            if('Rain' in j['condition']['text'])or('rain' in j['condition']['text']):
                
                st += j['time']+" : "+j['condition']['text'] + "\n"
                
    return st


# In[104]:


print_if_rain(x)


# In[105]:


def geo(name):
    geolocator = Nominatim(user_agent="my_app_name") # Replace "my_app_name" with your own user agent string
    location = geolocator.geocode(name)
    s = "Lat: "+str(location.latitude)+" Long: "+str(location.longitude)
    global lat,long
    lat = location.latitude
    long = location.longitude
    return s
def get_update(api_key,lat,long):
    lat = str(lat)
    long = str(long)
    complete_url = "https://api.weatherapi.com/v1/forecast.json?key="+api_key+"&q="+lat+","+long+"&days=2&aqi=no&alerts=yes"
    response = requests.get(complete_url)
    x = response.json()
    return x
import os
import telebot
bot = telebot.TeleBot('6152226003:AAEjC2XiqSmZhc-WQHBBNBawfC3BOwWvkd8')
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "For More Options /SmartIrrigation")
@bot.message_handler(commands=['SmartIrrigation'])
def irrigation_handler(message):
    text = "1.Temperature and Humidity\n2.Weather Overview\n3.Rain Forecast\n4.Rain Check\n5.Update Location"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, msg_handler)
    


# In[3]:


def check_temp_humidity():
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if humidity is not None and temperature is not None:
        s = "Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature,humidity)
        return s
    else:
        s = "Sensor Failure. Check Wiring"
        return s
def check_rain():
    no_rain = InputDevice(4)
    if not no_rain.is_active:
        s = "It's Raining"
        return s
    else:
        s = "Not Raining"
        return s


# In[4]:


def location_handler(message):
    bot.send_message(message.chat.id, geo(message.text))
def msg_handler(message):
    choice = message.text
    if choice == "1":
        bot.send_message(message.chat.id, check_temp_humidity())
    elif choice == "2":
        x = get_update(api_key,lat,long)
        bot.send_message(message.chat.id, print_weather_condition_by_day(x))
    elif choice == "3":
        x = get_update(api_key,lat,long)
        bot.send_message(message.chat.id, print_if_rain(x))
    elif choice == "4":
        x = get_update(api_key,lat,long)
        bot.send_message(message.chat.id,check_rain())
    elif choice == "5":
        text = "Enter Location"
        sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(sent_msg, location_handler)

chat_id = '1624381330'
import threading
import telebot
from gpiozero import InputDevice
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)
rain_sensor = InputDevice(17)
rain_started = False
soil_started = False
def rain_detection():
    global rain_started
    while True:
        if not rain_sensor.is_active:
            if not rain_started:
                bot.send_message(chat_id, "It's raining!")
                rain_started = True
        else:
            if rain_started:
                bot.send_message(chat_id, "The rain has stopped.")
                rain_started = False
        time.sleep(1)

def soil_sensor():
    global soil_started
    while True:
        if GPIO.input(channel):
            if not soil_started:
                bot.send_message(chat_id, "Soil moisture level is low")
                soil_started = True
        else:
            if soil_started:
                bot.send_message(chat_id, "Soil moisture level is good")
                soil_started = False
        time.sleep(1)
    
def telegram_bot():
    bot.polling(none_stop=True)

rain_thread = threading.Thread(target=rain_detection)
soil_thread =  threading.Thread(target=soil_sensor)
telegram_thread = threading.Thread(target=telegram_bot)
rain_thread.start()
soil_thread.start()
telegram_thread.start()
