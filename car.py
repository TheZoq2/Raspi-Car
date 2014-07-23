#Imports
import RPi.GPIO as GPIO
import time
import os

#variables
steeringPin = 15 
motorPin = 18

GPIO.cleanup()

#Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(steeringPin, GPIO.OUT)
GPIO.setup(motorPin, GPIO.OUT)

steeringPWM = GPIO.PWM(steeringPin, 50)
motorPWM = GPIO.PWM(motorPin, 50)


currentDuty = 4.0 
leftDuty = 4.5
rightDuty = 9 
neutralDuty = 7.1

forwardDuty = 10.0
backDuty = 5.0

steeringPWM.start(neutralDuty)
motorPWM.start(0)
try:
  running = True
  while(running == True):
    cmd = raw_input("Cmd: ")
    
    if(cmd == "f"):
      motorPWM.ChangeDutyCycle(forwardDuty)
    if(cmd == "s"):
      motorPWM.ChangeDutyCycle(0)
    if(cmd == "b"):
      motorPWM.ChangeDutyCycle(backDuty)
    if(cmd == "l"):
      steeringPWM.ChangeDutyCycle(leftDuty)
    if(cmd == "r"):
      steeringPWM.ChangeDutyCycle(rightDuty)
    if(cmd == "n"):
      steeringPWM.ChangeDutyCycle(neutralDuty)
    
    if(cmd == "exit"):
      running = False
except KeyboardInterrupt:
  pass

steeringPWM.stop()
motorPWM.stop()

GPIO.cleanup()

