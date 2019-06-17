import sys
sys.path.append('./memebot/features')
sys.path.append('./memebot/dictionaries')
sys.path.append('./memebot')

import global_vars
import bot_reply

import requests
import time


token = global_vars.token
groupID = global_vars.groupID
botID = global_vars.botID

requestParams = {'token': token, 'limit':1}

def app():
    while True:
        rqResponse = requests.get('https://api.groupme.com/v3/groups/' + groupID +'/messages', params = requestParams)
    
        # Pings the gm-membot Heroku app so it doesn't idle.
        requests.get('http://gm-memebot.herokuapp.com') 
    
        if rqResponse.status_code == 200:
            gotten = rqResponse.json()['response']['messages']
        
            for message in gotten:
                messageText = message['text'].lower()
                      
                if (messageText in bot_reply.staticTriggers) or (messageText in bot_reply.dynamicTriggers):
                    bot_reply.botReply(message)
                    requestParams['since_id'] = message['id']
        
        else:
            raise Exception('GroupMe\'s API fucked up.')
            break
    
    
        time.sleep(5)

app = app()
