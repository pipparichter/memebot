import sys
sys.path.append('../dictionaries')
sys.path.append('../')

import global_vars
import bot_reply

import os
import requests
import matplotlib.pyplot as plt 
import re

import boto3 
s3 = boto3.client('s3')

token = global_vars.token 
groupID = global_vars.groupID

bucketName = 'gm-memebot'


def picToURL(pathString):
    headers = {'X-Access-Token':token,'Content-Type': 'image/png'}

    # If, for whatever reason, you forget how the with statement works, check out this link: https://effbot.org/zone/python-with-statement.html.
    with open(pathString, 'rb') as image:
        binaryImage = image.read()

    response = requests.post('https://image.groupme.com/pictures', data = binaryImage, headers = headers, params = {'access_token':token})
    
    return response.json()['payload']['picture_url'] + '.large'




# Counts the number of times a word has been mentioned in the 1000 messages. 
def countWords(wordsToMatch):
    primaryCount = []
    cumulative = 0
    
    requestParams = {'token':token,'limit':100}
    
    while len(primaryCount) < 1000:    
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
    # formatted = [go.Scatter(x = [a for a in range(len(data))], y = data)]
    # graph = plotly.offline.plot({'data':formatted, 'layout':go.Layout(title = 'use of words' + ' ' + str(wordsToMatch))})
    
    plt.plot([a for a in range(len(data))], data)
    plt.xlabel('messages')
    plt.ylabel('cumulative word instances')
    plt.title('instances of the words ' + str(wordsToMatch))
    
    try:
        os.mkdir('../../tmp')
    except: FileExistsError
        pass 
    
    if os.path.exists('../../tmp'):
        bot_reply.sendMessage('directory creation successful')
    else:
        bot_reply.sendMessage('directory creation unsuccessful')
        return False

    plt.savefig('../../tmp/graph.png')
    
    if os.path.exits('../../tmp/graph.png'):
        bot_reply.sendMessage('save successful')
    else:
        bot_reply.sendMessage('save unsuccessful')
        return False

    s3.upload_file('../../tmp/graph.png', bucketName, 'graph.png')
    
    return True


def wordFrequency():
    bot_reply.sendMessage('sure thing, which words? (comma separated, please)')
    words = bot_reply.readReply()

    if ', ' in words:
        wordsToMatch = words.split(', ')

    elif ',' in words:
        wordsToMatch = words.split(',')

    else:
        return 'seriously, i said comma separated.'

    data = countWords(wordsToMatch)
    working = plotData(data, wordsToMatch)

    if working:
        return 'ok'
    else:
        return 'not ok'  
    
    # url = picToURL('../../tmp/graph.png')
    # if len(url) == 0:
        # return 'no url'
    # return url 
