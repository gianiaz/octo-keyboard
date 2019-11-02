import requests 
import sys
import time
import datetime
from requests.models import PreparedRequest

class ApiClient: 
    def __init__(self, host, apiKey, step): 
        self.host = host
        self.apiKey = apiKey
        self.step = str(step)
        self.moovementSpeed = "3600"
        self.lastMonitor = int(time.time())
        self.req = PreparedRequest()
        print "last monitor: "+ datetime.datetime.fromtimestamp(self.lastMonitor).strftime('%Y-%m-%d %H:%M:%S')
    def connect(self):
        print('Trying to connect')    
        response =  self.__post(
            '/connection', 
            {
                "command": "connect",
                "port": "/dev/ttyACM0",
                "baudrate": 115200,
                "printerProfile": "ende3",
                "save": True,
                "autoconnect": True
            }
        )
        strippedResult = {}
        strippedResult["isError"] = False
        if response["isError"]:
            strippedResult["isError"] = True
        if response["body"] == 'Printer is not operational':
            strippedResult["isError"] = True         
        return strippedResult

    def canPowerOnOrOff(self, printerRelay):
        if printerRelay.isOn and self.__askIfItsPrinting:
            print "Power can't be toggled now"
            return False

        print "Power can be toggled now"
        return True

    def monitorConnection(self):
        if(self.lastMonitor < (int(time.time()) - 30)):
            print "last monitor: "+ datetime.datetime.fromtimestamp(self.lastMonitor).strftime('%Y-%m-%d %H:%M:%S')
            print "check against: "+ datetime.datetime.fromtimestamp((int(time.time()) - 10)).strftime('%Y-%m-%d %H:%M:%S')
            if self.isOn():
                self.lastMonitor = int(time.time())
                res = self.__get('/connection')
                print res


    def isOn(self):
        print('Requiring printer power status')
        return self.__askIfItsOn()
    def isPrinting(self):
        print('Requiring printing status')
        return self.__askIfItsPrinting()
    def acceptCommands(self):
        print('Requiring availability for commands...')
        if (self.__askIfItsOn() and not self.__askIfItsPrinting()): 
            print "Printing..."
            return False

        print "Ok, send your commands"            
        return True

    def homePlate(self):
        print('HOME plate')
        self.__post('/printer/printhead', {"command": "home", "axes": ["x","y"]})
    def homeZ(self):
        print('HOME Z')
        self.__post('/printer/printhead', {"command": "home", "axes": ["z"]})
    def downZ(self):
        print('Down Z')
        #self.__post('/printer/printhead', {"command": "home", "axes": ["z"]})
    def rightXPlate(self):
        print('Right X plate')
        self.__G1Command('X', '')
    def leftXPlate(self):
        print('Left X plate')
        self.__G1Command('X', '-')
    def forwardYPlate(self):
        print('Forward Y plate')
        self.__G1Command('Y', '')
    def backwardYPlate(self):
        print('Backward Y plate')
        self.__G1Command('Y', '-')
    def disableSteppers(self):
        print('Disable steppers')
        #self.__G1Command('X', '')
    def extrude(self):
        print('Extrude')
        #self.__G1Command('X', '')
    def retract(self):
        print('Retract')
        #self.__G1Command('X', '')
    def light(self):
        print('Light')
        #self.__G1Command('X', '')
    def unloadFilament(self):
        print('unloadFilament')
        #self.__G1Command('X', '')
    def loadFilament(self):
        print('unloadFilament')
        #self.__G1Command('X', '')
    def upZ(self):
        print "Up z"       
        self.__G1Command('Z', '')

    def status(self):
        result = self.__get('/printer?exclude=temperature,sd')
        if not result["isError"]:
            return result["body"]["state"]["text"]

    def job(self):
        return self.__get('/job');


    def __askIfItsOn(self):
        result = self.__get('/printer?exclude=temperature,sd')
        return not result["isError"]

    def __askIfItsPrinting(self):
        result = self.__get('/printer?exclude=temperature,sd')
        if not result["isError"]:
            return result["body"]["state"]["flags"]["printing"]

    def __G1Command(self, axis, direction):
        result = self.__post('/printer/command', {"commands": ["G91","G1 "+axis+direction+self.step+" F"+self.moovementSpeed]})

    def __post(self, path, data):
        url = self.host+'/api' + path
        headers = {"x-api-key": self.apiKey}
        r = requests.post(url, headers= headers, json=data)

        response = {}
        response["code"] = r.status_code
        response["isError"] = False

        if r.status_code > 399: 
            response["isError"] = True
            response["body"] = r.content
            return response

        response["body"] = r.content
        return response

    def __get(self, path):
        url = self.host+'/api' + path;
        self.req.prepare_url(url, {'apikey':self.apiKey});
        url = self.req.url
        print('Requested url: '+ url)
        r = requests.get(url)

        response = {}
        response["code"] = r.status_code
        response["isError"] = False

        if(r.status_code > 399) :
            response["isError"] = True
            response["body"] = r.content
            return response
            
        response["body"] = r.json()
        return response

