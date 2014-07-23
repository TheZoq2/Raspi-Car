import tornado.ioloop
import tornado.web
import tornado.websocket

import string
import time
import os
import RPi.GPIO as GPIO
from subprocess import call

#defining some variables
steeringPin = 15
motorPin = 18

#For software PWM
leftDuty = 4.5
neutralDuty = 7.1
rightDuty = 9

forwardDuty = 10
backwardDuty = 5

#for servoblaster PWM
servodPath = "/home/frans/Documents/servoblaster/servoblaster/user/servod"
servodWritePath = "/dev/servoblaster"
leftPulse = 1000 #in prorcent
neutralPulse = 1500
rightPulse = 2000
steerServoID = 0

forwardPulse = 2000
backwardPulse = 1000
dirServoID = 1;

freq = 50

#Setting up GPIO
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(steeringPin, GPIO.OUT)
#GPIO.setup(motorPin, GPIO.OUT)

#steeringPWM = GPIO.PWM(steeringPin, freq)
#motorPWM = GPIO.PWM(motorPin, freq)

#Used to parse a message 
def parseMessage(message):
    #print("Parsing message");
    colonPos = string.find(message, ":")

    variable = []

    variable.append(message[0:colonPos])
    variable.append(message[colonPos + 1:])

    return variable;


def setDuty(amount):
    duty = 0
    if(amount == 0.5):
        duty = neutralDuty
    if(amount > 0.5 and amount <= 1):
        dutyDiff = rightDuty - neutralDuty
        duty = neutralDuty + dutyDiff * amount - 0.5
    if(amount < 0.5 and amount >= 0):
        dutyDiff = neutralDuty - leftDuty
        duty = leftDuty + dutyDiff * amount

    steeringPWM.ChangeDutyCycle(duty)

def setWheelPWM(amount):
    pulse = 0
#    if(amount == 0.5):
#        pulse = neutralPulse
#    if(amount > 0.5 and amount <= 1):
#        pulseDiff = rightPulse - neutralPulse
#        pulse = neutralPulse + pulseDiff * amount - 0.5
#    if(amount < 0.5 and amount >= 0):
#        pulseDiff = neutralPulse - leftPulse
#        pulse = leftPulse + pulseDiff * amount*/
    pulse = 0;
    if(amount >= 0 and amount <= 1):
        pulseDiff = rightPulse - leftPulse
        pulse = leftPulse + pulseDiff * amount

    #setting the pulse
    #call("echo 1=&fus > /dev/servoblaster" % pulse)
    os.system("echo %i=%fus > /dev/servoblaster" % (steerServoID, pulse))

def setDir(value):
    pulse = 0
    if value > 0.5:
        pulse = forwardPulse
    if value < 0.5:
        pulse = backwardPulse

    driveString = "echo %i=%fus > /dev/servoblaster" % (dirServoID, pulse)
    #print driveString
    os.system(driveString)

#defining classes
class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Client connected")

    def on_message(self, message):
        #Reading messages
        print(message)

        #parse the message
        parsedMsg = parseMessage(message)
        
        if(parsedMsg[0] == "driveDir"):
            value = float(parsedMsg[1])

            setDir(value);

        if(parsedMsg[0] == "turnAmount"):
            #Getting the position of the : which divides the string between variable name and value
            value = float(parsedMsg[1])

            setWheelPWM(value)


    def on_close(self):
        pass


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.write("RPI controller, go to <a href='static/index.html'>/static/index.html</a>");

class Files(tornado.web.RequestHandler):
    def get(self,File_Name):
        if(File_Name.find(".css") != -1):
            self.set_header("Content-type", "text/css")
            print("Sending .css file")

        File = open(File_Name,"r")
        self.write(File.read())
        File.close()

    def post(self,File_Name):
        File = open(File_Name,"r")
        self.write(File.read())
        File.close()

#Setting up
#Open a GPIO port
#GPIO.SetMode


try:
    #Starting the steering
    #steeringPWM.start(leftDuty)

    #Start the servo program
    os.system("sudo %s --p1pins=16,18" % servodPath)

    application = tornado.web.Application([
        (r"/", Main),
        (r"/websocket", SocketHandler),
        (r"/(.*)",Files)
    ])

    if __name__ == "__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    pass

#cleanup
os.system("echo 0=0us > /dev/servoblaster")
os.system("echo 1=0us > /dev/servoblaster")
#steeringPWM.ChangeDutyCycle(neutralDuty)

#motorPWM.stop()
#steeringPWM.stop()

print("Exiting server")