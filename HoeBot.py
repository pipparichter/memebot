import requests
import time

import global_vars
import triggers 
    

token = global_vars.token
groupID = global_vars.groupID
botID = global_vars.botID

# 
def botReply(message):
    
    triggers.senderID = message['sender_id']
    triggers.messageID = message['id']
    
    messageText = message['text'].lower()

    if messageText == 'meme me':
        reply = triggers.memeGenerator()
        
    # if messageText == 'joke me':
        # reply = triggers.jokeGenerator()
        
    elif messageText == 'word frequency me':
        reply = triggers.yeet()

    else:
        reply = triggers.staticTriggers[messageText]
        
    triggers.sendMessage(reply)
    return      
    
    
###########################################################################################################################################################

requestParams = {'token': token, 'limit':1}

while True:
    rqResponse = requests.get('https://api.groupme.com/v3/groups/' + groupID +'/messages', params = requestParams)
    
    if rqResponse.status_code == 200:
        gotten = rqResponse.json()['response']['messages']
        
        for message in gotten:
            messageText = message['text'].lower()
                      
            if (messageText in triggers.staticTriggers) or (messageText in triggers.dynamicTriggers):
                botReply(message)
                requestParams['since_id'] = message['id']
        
    else:
        raise Exception('GroupMe\'s API fucked up.')
        break
    
    
    time.sleep(5)