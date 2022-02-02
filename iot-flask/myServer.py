
import time
import datetime

import threading

import mqttPublish
import mqttSubscribe


class myServer():
    # a dict of mqtt channels with their current value
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData ={
        'serverTime': timeString,
        'mqttDict': {
            '/huzzah1/time': '',
            '/huzzah1/button1': False,
            '/huzzah1/value1': 12,
        }
    }

    def __init__(self):
        self.sub=threading.Thread(target=mqttSubscribe.run)
        self.sub.deamon = True
        #self.sub.start()
    
    def getState(self):
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        return self.templateData

    def setState(self, device, topic, action):
        folder = '/' + device + '/' + topic
        if not folder in self.templateData['mqttDict'].keys():
            print(f'ERROR: setState() did not find folder "{folder}"')
        else:
            newValue = action
            if newValue == 'toggle':
                newValue = not self.templateData['mqttDict'][folder]  # assuming True/False
            self.templateData['mqttDict'][folder] = newValue
            print(f'setstate() {folder} value is now "{newValue}"')
        return self.templateData

    def setState2(self, folder, action):
        if not folder in self.templateData['mqttDict'].keys():
            print(f'ERROR: setState() did not find folder "{folder}"')
        else:
            newValue = action
            if newValue == 'toggle':
                newValue = not self.templateData['mqttDict'][folder]  # assuming True/False
            self.templateData['mqttDict'][folder] = newValue
            print(f'setstate() {folder} value is now "{newValue}"')
        return self.templateData

if __name__ == '__main__':
    ms = myServer()

    print('myServer() entering infinit loop')
    while True:
        time.sleep(0.01)  # sleep for 10 ms
