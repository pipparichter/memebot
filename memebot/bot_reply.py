# This module includes basic functions which allow MemeBot to interact with the designated groupchat. Capabilities provided includes
# reading messages, sending messages, and generating a reply based on the read messages. This module also includes the list of static
# and dynamic triggers. 


# Include subpackages in the sys.path so contained modules may be imported. 
import sys
sys.path.append('./dictionaries')
sys.path.append('./features')

import global_vars
import meme_generator

import requests
import re
import time


# ONCE THE BOT IS WORKING PROPERLY, TRY TO FIGURE OUT A WORKAROUND SO I DON'T NEED GLOBAL VARIABLES (POOR CODING PRACTICE). 
botID = global_vars.botID
groupID = global_vars.groupID
token = global_vars.token


staticTriggers = {
        'hello, memebot':'hey bitches',
        'thanks, memebot':'don\'t mention it',
        'memebot, do you have anything to say to adam?':'yes. leave'
        }

dynamicTriggers = [
        'meme me',
        'memebot, tell me a joke'
        ]


# This function takes a string as an argumument (the string may be a message or the URL for an image) and sends the message or image
# or message text into the designated GroupMe. **The image URL must be returned from the GroupMe image service. The pic_to_url module
# in the master directory will take a regular image URL and return one in the picStructure format.**
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
# PYTHON MAY NOT LIKE THE ORDER OF VARIABLE ASSIGNMENTS IN THIS MODULE-- IF THE PARSER THROWS AN ERROR REGARDING THE VARIABLES,
# THAT'S PROBABLY WHY. 
def readReply():
    messageID = readReply.messageID
    senderID = readReply.senderID
    
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

# 
def botReply(message):

    senderID = message['sender_id']
    messageID = message['id']
    
    readReply.senderID = senderID
    readReply.messageID = messageID

    messageText = message['text'].lower()

    if messageText == 'meme me':
        reply = meme_generator.memeGenerator()
 
    # if messageText == 'joke me':
        # reply = triggers.jokeGenerator()

    # elif messageText == 'word frequency me':
        # reply = word_counter.____()

    else:
        reply = staticTriggers[messageText]

    sendMessage(reply)
    return

