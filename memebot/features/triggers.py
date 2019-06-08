# import yeeter_meter as yeet
import meme_dict as memes
# import joke_lib as jokes
import global_vars

import requests
import random
import re
import time


token = global_vars.token
groupID = global_vars.groupID
botID = global_vars.botID

senderID = ''
messageID = ''

#
def sendMessage(toSend):
    text = ''
    attachment = None
    
    picStructure = 'https://i.groupme.com/[\d]+x[\d]+.[\D]{2,3}.[\w]+'
    
    if type(re.compile(picStructure).match(toSend)) != type(None):
        attachment = toSend
        text = 'here ya go'
    else:
        text = toSend
            
    postParams= {'bot_id':botID}
    postData = {'text':text, 'picture_url': attachment}
        
    requests.post('https://api.groupme.com/v3/bots/post', data = postData, params = postParams)
    return
    

# This function takes a sender ID and message ID and returns the next message by the same sender.
def readReply():
    t = 0
    requestParams = {'since_id':messageID, 'token':token, 'limit':20}
    
    while t < 3:

        rawResponse = requests.get('https://api.groupme.com/v3/groups/' + groupID +'/messages', params = requestParams)
        
        gotten = rawResponse.json()['response']['messages']
        
        for message in gotten:
            if (message['id'] > messageID) and (message['sender_id'] == senderID):
                print(message['text'])
                return message['text'].lower()
        
        time.sleep(5)
        t += 1
        
    return 0
              

##########################################################################################################################################

# This function contains the procedure needed for the user to specify a category of meme, to be sent into the designated group chat. 
def memeGenerator():
    
    categories = [key for key in memes.memeLib.keys()]
    
    sendMessage('heck ya, what category of meme? (nerdy, wholesome, inside jokes)')
    
    reply = readReply()
    
    if reply == 0:
        return 'oops, your meme request timed out. get it together and try again.'
    else:
        if reply in categories:
            memeList = memes.memeDict[reply]
            return random.choice(memeList)
        else:
            return 'oops, you didn\'t respond with a valid category of meme. get it together and try again.'
        
            
# def yeetGenerator():
    # wordsToMatch = 
    # frequency = yeet.wordFrequency(wordsToMatch)
    
    


# def jokeGenerator():           

    
staticTriggers = {
'hello, hoebot':'hello, bitches',
'thanks, hoebot':'don\'t mention it'
}

dynamicTriggers = {
'meme me', 
'tell me a joke, hoebot',
'word frequency me'
}
