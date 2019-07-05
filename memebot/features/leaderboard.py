# Things to include in the leaderboard: total likes, total messages, likes per message, messages liked(?).

# import Cython

import sys
sys.path.append('../')
sys.path.append('../../')

import requests
import json
import pandas as pd
import numpy as np

import boto3
s3 = boto3.client('s3')
from botocore.exceptions import ClientError

# import bot_reply
import global_vars

token = global_vars.token
groupID = global_vars.groupID 
# The group ID for Caltech Commies '23 is '50201122'

bucketName = 'gm-memebot'

# The GroupMe API allows apps to get a maximum of 100 messages per request.
requestParams = {'token':token, 'group_id':groupID, 'limit':100}



# Tries to load data, assuming a leaderboard_data.txt file is saved in the AWS bucket. If no file exits, an empty dataframe
# structure is returned, of the format {'stop':MESSAGE_ID, 'data':{'person1':{'likes':INT, 'messages':INT}, 'person2'...}.
def loadData():
    try:
        response = s3.get_object(Bucket = bucketName, Key = 'leaderboard_data.txt')['Body']
        data = response.read().decode('utf-8')
        pyObject = json.loads(data)

    # A ClientError occurs when the file does not exist in the AWS bucket.
    except ClientError:
        # If no file exits, assign an empty data structure to pyObject.
        pyObject = {'data':{}, 'stop':None}
    
    return pyObject



# If a leaderboard exists, the corresponding data. If not, load new data.
def getStats():
    oldData = loadData()
    data = oldData['data']
    stop = oldData['stop'] 

    runOnce = False
    end = False
    
    # Slightly dangerous while loop, make sure this doesn't become infinite.
    while not end:
        response = requests.get('https://api.groupme.com/v3/groups/' + groupID + '/messages', params = requestParams)
 
        try:
            messages = response.json()['response']['messages']
        
        # The JSONDecodeError arises when there aren't enough messages in the group.
        except json.decoder.JSONDecodeError:
            try:
                # Reduce the number of messages being requested at once so every message in the groupchat can be accounted for.
                requestParams['limit'] = 1
                response = requests.get('https://api.groupme.com/v3/groups/' + groupID + '/messages', params = requestParams)
                messages = response.json()['response']['messages']
            
            except json.decoder.JSONDecodeError:
                break
        
        # The before_id tells the GroupMe API to return messages before the given message ID, in DESCENDING ORDER, i.e.
        # the newest messages first (I tested this).
        requestParams['before_id'] = messages[-1]['id']

        for message in messages:
            # If the message ID matches the ID of the most recent message from the last time the getstats() function
            # was called, break out of both the for loop and while loop.
            if message['id'] == stop:
                end = True

                break
        
            person = message['name']
           
            if person not in data:
                data[person] = {'messages':1, 'likes':len(message['favorited_by'])}
                    
            else:
                data[person]['messages'] += 1
                data[person]['likes'] += len(message['favorited_by'])
        
        # Stores the message ID of the most recent message in the groupchat when the function is called.
    if not runOnce:
            stopReference = messages[0]['id']
            runOnce = True 
                              

    newData = {'stop':stopReference, 'data':data}

    return newData



# Create a pandas DataFrame containing the data returned by getStats(). The intended argument is getStats()['data'].
def leaderboard(data):
    
    people = np.array([]) 
    likes = np.array([])
    messages = np.array([])

    for person in data:
        people = np.append(people, person)
        likes = np.append(likes, data[person]['likes'])
        messages = np.append(messages, data[person]['messages'])
    
    formattedData = {'USER':people, 'TOTAL MESSAGES':messages, 'TOTAL LIKES':likes, 'LIKES PER MESSAGE':likes/messages}
    board = pd.DataFrame(formattedData)
    
    return board



# Upload the new or updated leaderboard data to the AWS bucket and save a temporary copy of the leaderboard as an html file 
# in the ~/tmp file.
# IMPORTANT: The data argument in this case includes the 'stop' key. 
def saveNew(data, board):
    # Files in the tmp directory SHOULD be deleted after the request has been made (according to a random 
    # StackOverflow post).
    # If not, I'll have to add in code to delete any preexisting files. 
    with open('/tmp/leaderboard.html', 'w') as lb:
        lb.write(board.to_html())

    with open('/tmp/leaderboard_data.txt', 'w') as lbd:
        lbd.write(str(data).replace('\'', '"'))
        
    s3.upload_file('/tmp/leaderboard_data.txt', bucketName, 'leaderboard_data.txt')
    s3.upload_file('/tmp/leaderboard.html', bucketName, 'leaderboard.html')

    return 'successful'
    

def generate():
    stats = getStats()
    saveNew(stats, leaderboard(stats['data']))

    return 'successful'

