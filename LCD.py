from RPLCD.i2c import CharLCD
import time

class LCDMenu: 
    def __init__(self, address, printerClient):
        self.lcd = CharLCD('PCF8574', address)
        self.printerClient = printerClient
        self.start = time.time()
        self.bounceTime = 1
        self.__printerStatus()
        print self.printerClient.status()
    def watch(self):
        if self.printerClient.isOn and int(self.start) + self.bounceTime < int(time.time()):
            self.start = time.time()
            self.__printerStatus()
    def __printerStatus(self):
        self.lcd.clear()
        print self.printerClient.status()
        self.lcd.write_string(self.printerClient.status())
        if(self.printerClient.isPrinting):
            jobInfo = self.printerClient.job()
            self.lcd.write_string(" s:" + time.strftime('%H:%M', time.gmtime(jobInfo["body"]["progress"]["printTime"])))



