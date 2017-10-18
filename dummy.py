import time
import json
from websocket import create_connection
import sys
sys.path.append(r"C:\Users\69390\Desktop\texas-holdem")
from deuces import Evaluator

# pip install websocket-client
ws = ""
def takeAction(action, data, name):
        
    if action == "__bet":
        #time.sleep(2)
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": name,
                "amount": 30
            }
        }))
    elif action == "__action":
        #time.sleep(2)
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "call",
                "playerName": name
            }
        }))
    
    
def doListen(name):
    
    try:
        global ws
#        ws = create_connection("ws://116.62.203.120")
        ws = create_connection("ws://thegame.trendmicro.com.cn")
        ws.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": name
            }
        }))
        while 1:
            result = ws.recv()
            msg = json.loads(result)
            event_name = msg["eventName"]
            data = msg["data"]
            print event_name
            print json.dumps(data)
            print "============"
            print "Dummy", name
            print "============"
            takeAction(event_name, data, name)
    except Exception, e:
        print e.message
        doListen(name)

if __name__ == '__main__':
    name = 'd9'
    doListen(name)
