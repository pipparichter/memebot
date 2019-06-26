import sys
sys.path.append('../dictionaries')
sys.path.append('../')

import global_vars

import requests
import matplotlib.pyplot as plt 
import re



token = global_vars.token 
groupID = global_vars.groupID


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
    
    plt.savefig('C:\\Users\\Pippa\\Desktop\\yeeter_meeter.png')
    
    return


def wordFrequency(wordsToMatch):
    data = countWords(wordsToMatch)
    graph = plotData(data, wordsToMatch)
    
    return graph
