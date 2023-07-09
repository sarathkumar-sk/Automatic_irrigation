from time import sleep
from gpiozero import Buzzer, InputDevice
 
buzz    = Buzzer(13)
no_rain = InputDevice(4)
 
def buzz_now(iterations):
    for x in range(iterations):
        buzz.on()
        sleep(0.1)
        buzz.off()
        sleep(0.1)
 
while True:
    if not no_rain.is_active:
        print("It's raining - get the washing in!")
        buzz_now(5)
    sleep(1)
