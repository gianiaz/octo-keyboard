#!/usr/bin/python
from Button import Button
from PrinterApiClient import ApiClient
import time
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')
print "Initializing api client"
client = ApiClient(config.get('api', 'host')+':'+config.get('api', 'port'), config.get('api', 'apikey'), config.get('api', 'step'))

print "Initializing buttons"
# 2
forwardYButton = Button(18, 'ForwardYButton', client.canExecuteCommands, client.forwardPlate)
# 6
leftButton = Button(16, 'LeftXButton', client.canExecuteCommands, client.leftPlate)
# 7
homeButton = Button(12, 'HomeXYButton', client.canExecuteCommands, client.homePlate)
# 8
rightButton = Button(22, 'RightXButton', client.canExecuteCommands, client.rightPlate)
# 12
backwardYButton = Button(11, 'ForwardYButton', client.canExecuteCommands, client.backwardPlate)

print "Starting main loop"
while True:
    homeButton.watch()
    rightButton.watch()
    leftButton.watch()
    forwardYButton.watch()
    backwardYButton.watch()