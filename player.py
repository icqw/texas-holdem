import json
from websocket import create_connection
import core
# pip install websocket-client
ws = ""
def takeAction(action, data, name):
    
    if action == "__bet":
        action = core.ai_action(data)
        if action == "fold":
            amount = 0
        if action == "call":
            amount = 20
        if action == "raise":
            amount = 100
        if action == "allin":
            amount = 200
            
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": name,
                "amount": amount
            }
        }))
    elif action == "__action":
        action = core.ai_action(data)
        
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": action,
                "playerName": name
            }
        }))
    
    
def doListen(name):
    '''
    try:
        global ws
        ws = create_connection("ws://116.62.203.120")
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
            data = json.dumps(data)
            print event_name
            #print data
            takeAction(event_name, data, name)
    except Exception, e:
        print e.message
        doListen(name)
    '''
    
    global ws
    ws = create_connection("ws://116.62.203.120")
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
        #data = json.dumps(data)
        print event_name
        #print data
        takeAction(event_name, data, name)    
    
        
if __name__ == '__main__':
    name = 'sparrow'
    doListen(name)
