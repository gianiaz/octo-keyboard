#!/usr/bin/python
from Button import Button
from PrinterApiClient import ApiClient
import time
from Relay import Relay
import ConfigParser
import sys
from Raspi import Raspi
from RPLCD.i2c import CharLCD
import LCD

config = ConfigParser.SafeConfigParser({'bounceTime': 0.2})
config.read('config.ini')

buttons = config.options('buttonKeyboard')

print "Initializing api client"
client = ApiClient(config.get('api', 'host')+':'+config.get('api', 'port'), config.get('api', 'apikey'), config.get('api', 'step'))

lcd = LCD.LCDMenu(0x3f, client);

raspi = Raspi()

print "Initializing buttons"
print "Initializing power relay"
powerStatus = True
if(not client.isOn()):
    print "Is OFF, trying to connect"
    res = client.connect()
    if res["isError"]:
       powerStatus = False
       print "Can't connect, the printer is offline (maybe is off?)"
    
printerRelay = Relay(
    int(
        config.get('relay', 'printer')
    )
    , 
    'printerRelay', 
    powerStatus
    )
printerRelay.setDebug(True)        

# 1
powerButton = Button(
    config.get('buttonKeyboard', 'power'), 
    config.getfloat('buttons', 'bounceTime'),
    'powerButton', 
    [client.canPowerOnOrOff, printerRelay], # todo logica pre-condizione per accendere e spegnere la stampante. 
    printerRelay.toggle
    )
powerButton.setDebug(True)    
# 2
forwardYPlateButton = Button(
    config.get('buttonKeyboard', 'forwardYPlate'), 
    config.getfloat('buttons', 'bounceTime'),
    'forwardYPlateButton', 
    client.acceptCommands, 
    client.forwardYPlate
    )    
forwardYPlateButton.setDebug(True)    
# 3
upZButton = Button(
    config.get('buttonKeyboard', 'upZ'), 
    config.getfloat('buttons', 'bounceTime'),
    'upZButton', 
    client.acceptCommands, 
    client.upZ
    )
upZButton.setDebug(True)    
# 4
retractButton = Button(
    config.get('buttonKeyboard', 'retract'), 
    config.getfloat('buttons', 'bounceTime'),
    'retractButton', 
    client.acceptCommands, 
    client.retract
    )
retractButton.setDebug(True)    
# 5
unloadFilamentButton = Button(
    config.get('buttonKeyboard', 'unloadFilament'), 
    config.getfloat('buttons', 'bounceTime'),
    'unloadFilamentButton', 
    client.acceptCommands, 
    client.unloadFilament
    )
unloadFilamentButton.setDebug(True)    
# 6
leftXPlateButton = Button(
    config.get('buttonKeyboard', 'leftXPlate'), 
    config.getfloat('buttons', 'bounceTime'),
    'leftXPlateButton', 
    client.acceptCommands, 
    client.leftXPlate
    )
leftXPlateButton.setDebug(True)    
# 7
homePlateButton = Button(
    config.get('buttonKeyboard', 'homePlate'), 
    config.getfloat('buttons', 'bounceTime'),
    'HomeXYButton', 
    client.acceptCommands, 
    client.homePlate
    )
homePlateButton.setDebug(True)    
# 8
rightXPlateButton = Button(
    config.get('buttonKeyboard', 'rightXPlate'), 
    config.getfloat('buttons', 'bounceTime'),
    'rightXPlateButton', 
    client.acceptCommands, 
    client.rightXPlate
    )
rightXPlateButton.setDebug(True)    
# 9
homeZButton = Button(
    config.get('buttonKeyboard', 'homeZ'), 
    config.getfloat('buttons', 'bounceTime'),
    'homeZButton', 
    client.acceptCommands, 
    client.homeZ
    )
homeZButton.setDebug(True)    
# 10
disableSteppersButton = Button(
    config.get('buttonKeyboard', 'disableSteppers'), 
    config.getfloat('buttons', 'bounceTime'),
    'disableSteppersButton', 
    client.acceptCommands, 
    client.disableSteppers
    )
disableSteppersButton.setDebug(True)    
# 11
lightButton = Button(
    config.get('buttonKeyboard', 'light'), 
    config.getfloat('buttons', 'bounceTime'),
    'lightButton', 
    client.acceptCommands, 
    client.light
    )    
lightButton.setDebug(True)    


# 12
backwardYPlateButton = Button(
    config.get('buttonKeyboard', 'backwardYPlate'), 
    config.getfloat('buttons', 'bounceTime'),
    'backwardYPlateButton', 
    client.acceptCommands, 
    client.backwardYPlate
    )    
backwardYPlateButton.setDebug(True)    
# 13
downZButton = Button(
    config.get('buttonKeyboard', 'downZ'), 
    config.getfloat('buttons', 'bounceTime'),
    'downZButton', 
    client.acceptCommands, 
    client.downZ
    )    
downZButton.setDebug(True)    
# 14
extrudeButton = Button(
    config.get('buttonKeyboard', 'extrude'), 
    config.getfloat('buttons', 'bounceTime'),
    'extrudeButton', 
    client.acceptCommands, 
    client.extrude
    )    
extrudeButton.setDebug(True)    
# = Button(18, 'ForwardYButton', client.canExecuteCommands, client.forwardPlate)
# 15
loadFilamenButton = Button(
    config.get('buttonKeyboard', 'loadFilament'), 
    config.getfloat('buttons', 'bounceTime'),
    'loadFilamenButton', 
    client.acceptCommands, 
    client.loadFilament
    )    
loadFilamenButton.setDebug(True)    


# 16
plusButton = Button(
    config.get('buttonKeyboard', 'plus'), 
    config.getfloat('buttons', 'bounceTime'),
    'plusButton', 
    client.acceptCommands, 
    raspi.plus
    )    
plusButton.setDebug(True)    

# 17
setButton = Button(
    config.get('buttonKeyboard', 'setLCD'), 
    config.getfloat('buttons', 'bounceTime'),
    'setButton', 
    client.acceptCommands, 
    raspi.confirm
    )    
setButton.setDebug(True)    

# 19
cancelButton = Button(
    config.get('buttonKeyboard', 'cancelLCD'), 
    config.getfloat('buttons', 'bounceTime'),
    'cancelButton', 
    client.acceptCommands, 
    raspi.cancel
    )    
cancelButton.setDebug(True)    

# 20
minusButton = Button(
    config.get('buttonKeyboard', 'minus'), 
    config.getfloat('buttons', 'bounceTime'),
    'minusButton', 
    client.acceptCommands, 
    raspi.minus
    )    
minusButton.setDebug(True)    



print "Starting main loop"
while True:
     #client.monitorConnection()
     #1
     powerButton.watch()
     #2 
     forwardYPlateButton.watch()
     #3
     upZButton.watch()     
     #4 
     retractButton.watch()
     #5 
     unloadFilamentButton.watch()
     #6
     leftXPlateButton.watch()
     #7
     homePlateButton.watch()
     #8
     rightXPlateButton.watch()
     #9
     homeZButton.watch()
     #9
     disableSteppersButton.watch()
     #11 
     lightButton.watch()
     #12
     backwardYPlateButton.watch()
     #13
     downZButton.watch()
     #14
     extrudeButton.watch()
     #15
     loadFilamenButton.watch()

     #16
     plusButton.watch()
     #17
     setButton.watch()
     #19
     cancelButton.watch()
     #20
     minusButton.watch()

     lcd.watch()
