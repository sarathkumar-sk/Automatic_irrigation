import Adafruit_DHT
import time
from gpiozero import Buzzer, InputDevice
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27
buzz    = Buzzer(13)
no_rain = InputDevice(4)

def buzz_now(iterations):
    for x in range(iterations):
        buzz.on()
        time.sleep(0.1)
        buzz.off()
        time.sleep(0.1)
 
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if not no_rain.is_active:
        print("It's raining - No need to water")
        buzz_now(5);
    else:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity));
    time.sleep(3);
