import sys
sys.path.append('../dictionaries')
sys.path.append('../')

import global_vars
import bot_reply

import requests
import matplotlib.pyplot as plt 
import re

token = global_vars.token 
groupID = global_vars.groupID


def picToURL(pathString):
    headers = {'X-Access-Token':token,'Content-Type': 'image/png'}

    # If, for whatever reason, you forget how the with statement works, check out this link: https://effbot.org/zone/python-with-statement.html.
    with open(pathString, 'rb') as image:
        binaryImage = image.read()

    response = requests.post('https://image.groupme.com/pictures', data = binaryImage, headers = headers, params = {'access_token':token})
    
    return response.json()['payload']['picture_url'] + '.large'


# Counts the number of times a word has been mentioned in the 100 messages. 
def countWords(wordsToMatch):
    primaryCount = []
    cumulative = 0
    
    requestParams = {'token':token,'limit':10}
    
    while len(primaryCount) < 100:    
        secondaryCount = []
          
        # Remember, according to GroupMe's API, "If before_id is provided, then messages immediately preceding the 
        # given message will be returned, in DESCENDING ORDER."
        
        response = requests.get('https://api.groupme.com/v3/groups/' + groupID +'/messages', params = requestParams).json()['response']['messages']
        requestParams['before_id'] = response[-1]['id']
        
        for message in response:
            messageText = message['text']
            
            if messageText != None:
                splitMessage = re.split('\W', messageText)
                
                for word in splitMessage:
                    if word in wordsToMatch:
                        cumulative += 1
                        
            secondaryCount.append(cumulative)
        primaryCount += secondaryCount
    
    return primaryCount
                
        
# Takes a list as input and returns a graph plotting the values of the list with respect to their corresponding indices. 
def plotData(data, wordsToMatch):    
    plt.plot([a for a in range(len(data))], data)
    plt.xlabel('messages')
    plt.ylabel('cumulative word instances')
    plt.title('instances of the words ' + str(wordsToMatch))
    
    plt.savefig('../../tmp/graph.png')
    
    return


def wordFrequency():
    bot_reply.sendMessage('sure thing, which words?')
    wordsToMatch = re.split('\W', bot_reply.readReply())

    data = countWords(wordsToMatch)
    plotData(data, wordsToMatch)

    url = picToURL('../../tmp/graph.png')
    
    return url 
