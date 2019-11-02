import RPi.GPIO as GPIO
import time

class Relay: 
    def __init__(self, pin, identifier, initialState): 
        self.pin = pin
        self.isOn = initialState
        self.identifier = identifier
        self.debug = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
    def init(self):
        if(self.debug):
            print self.identifier+": Initial state is "+str(self.isOn)
        else:
            if self.isOn:
                GPIO.output(self.pin, GPIO.HIGH)
            else:     
                GPIO.output(self.pin, GPIO.LOW)
    def setDebug(self, debug): 
        self.debug = debug
    def toggle(self):
        print self.isOn
        self.isOn = not self.isOn
        print self.isOn
    def isOn(self):
        return self.isOn
                


