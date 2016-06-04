import tornado.ioloop
import tornado.web
import tornado.websocket

import string
import time
import os
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
servodPath = "/home/frans/Documents/PiBits/ServoBlaster/user/servod"
servodWritePath = "/dev/servoblaster"
leftPulse = 1000 #in prorcent
neutralPulse = 1500
rightPulse = 2000
steerServoID = 0

forwardPulse = 2000
backwardPulse = 1000
dirServoID = 1;

freq = 50

#Used to parse a message 

def setWheelPWM(amount):
    pulse = 0
    if(amount >= 0 and amount <= 1):
        pulseDiff = rightPulse - leftPulse
        pulse = leftPulse + pulseDiff * amount

    print("Chanaging turn direction to {}", amount);
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
        parsedMsg = message.split(":")
        
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


try:
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

print("Exiting server")
