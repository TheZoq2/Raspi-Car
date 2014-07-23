#Imports
import RPi.GPIO as GPIO
import time
import os

#variables
steeringPin = 18
motorPin = 15

GPIO.cleanup()

#Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(steeringPin, GPIO.OUT)
GPIO.setup(motorPin, GPIO.OUT)

steeringPWM = GPIO.PWM(steeringPin, 50)
motorPWM = GPIO.PWM(motorPin, 50)


currentDuty = 5.0 

steeringPWM.start(currentDuty)
motorPWM.start(currentDuty)
try:
  pass
  while(currentDuty < 10.0):
    os.system("clear")
    steeringPWM.ChangeDutyCycle(currentDuty)
    motorPWM.ChangeDutyCycle(currentDuty)
    print("Current duty %f" % currentDuty)
    time.sleep(0.1)
    currentDuty = currentDuty + 0.1

except KeyboardInterrupt:
  pass

steeringPWM.stop()
motorPWM.stop()

GPIO.cleanup()

