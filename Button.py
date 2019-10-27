import RPi.GPIO as GPIO


class Button: 
    def __init__(self, buttonPin, identifier, preCondition, command): 
        GPIO.setmode(GPIO.BOARD)
        self.buttonPin = buttonPin
        self.preCondition = preCondition
        self.command = command
        self.identifier = identifier
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        print self.identifier + ': initialized'
    def watch(self):
        if self.__isPressed():
            print self.identifier + ': checking preconditions'
            if self.preCondition():
                print self.identifier + ': issuing command'
                self.command()
    def __isPressed(self):
          return GPIO.input(self.buttonPin) == GPIO.HIGH
