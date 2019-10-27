import requests 

class ApiClient: 
    def __init__(self, host, apiKey, step): 
        self.host = host
        self.apiKey = apiKey
        self.step = str(step)
        self.moovementSpeed = "3600"
    def canExecuteCommands(self):
        print('Requiring printing status')
        result = self.__request('/printer?exclude=temperature,sd', 'GET', {})
        return not result["state"]["flags"]["printing"]
    def homePlate(self):
        print('HOME plate')
        result = self.__request('/printer/printhead', 'POST', {"command": "home", "axes": ["x","y"]})
    def rightPlate(self):
        print('Right X plate')
        self.__G1Command('X', '')
    def leftPlate(self):
        print('Left X plate')
        self.__G1Command('X', '-')
    def forwardPlate(self):
        print('Forward Y plate')
        self.__G1Command('Y', '')
    def backwardPlate(self):
        print('Backward Y plate')
        self.__G1Command('Y', '-')

    def __G1Command(self, axis, direction):
        result = self.__request('/printer/command', 'POST', {"commands": ["G91","G1 "+axis+direction+self.step+" F"+self.moovementSpeed]})

    def __request(self, path, method, data):
        url = self.host+'/api' + path
        if(method == "POST"):
            headers = {"x-api-key": self.apiKey}
            print data
            print headers
            r = requests.post(url, headers= headers, json=data)
        else:
            url = url + '&apikey=' + self.apiKey
            print('Requested url: '+ url)
            r = requests.get(url)

        if(r.status_code > 399) :
            print "Porcodidio non funziona"
            return

        if r.content: 
            return r.json()

