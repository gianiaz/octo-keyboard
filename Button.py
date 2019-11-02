import RPi.GPIO as GPIO
import time
import traceback

class Button: 
    def __init__(self, buttonPin, bounceTime, identifier, preCondition, command): 
        GPIO.setmode(GPIO.BOARD)
        self.buttonPin = int(buttonPin)
        self.bounceTime = bounceTime
        self.preCondition = preCondition
        self.command = command
        self.identifier = identifier    
        self.debug = False
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        print self.identifier + ': initialized on pin '+ str(self.buttonPin)
    def setDebug(self, debug): 
        self.debug = debug
    def watch(self):
        if self.__isPressed():
            print self.identifier + ': checking preconditions'
            if type(self.preCondition) == list:
                print self.identifier + ': is a list'
                f = self.preCondition[0]
                arg = self.preCondition[1]
                if not f(arg) and not self.debug:
                    return 
                print self.identifier + ': issuing command'
                if self.debug:
                    print self.identifier + ': '+ traceback.extract_stack(None, 2)[0][2]
                else: 
                    self.command()                    
                time.sleep(self.bounceTime)
            else:
                print self.identifier + ': is not a list'
                if not self.debug and self.preCondition():
                    print self.identifier + ': issuing command'
                    if self.debug:
                        print self.identifier + ': '+ traceback.extract_stack(None, 2)[0][2]
                    else: 
                        self.command()                    
                    time.sleep(self.bounceTime)

    def __isPressed(self):
        if GPIO.input(self.buttonPin) == GPIO.HIGH:
            print self.identifier + ": isPressed"
        return GPIO.input(self.buttonPin) == GPIO.HIGH
