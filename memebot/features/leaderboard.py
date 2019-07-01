# Things to include in the leaderboard: total likes, total messages, likes per message, messages liked(?).

# import Cython

import sys
sys.path.append('../')

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

requestParams = {'token':token, 'group_id':groupID, 'limit':100}


# Tries to load data, assuming a leaderboard_data.txt file is saved in the AWS bucket.
def loadData():
   response = s3.get_object(Bucket = bucketName, Key = 'leaderboard_data.txt')['Body']
   data = response.decode('utf-8')
   dataAsPyObject = json.loads(data)

   return dataAsPyObject
    

# If a leaderboard exists, update it. If not, create a new leaderboard.
def getStats():
    try:
        # This dictionary contains a every person in the groupchat who has sent a message in the last 1000 messages as keys
        # (or 10000 depending on how long the code takes to run). The values are also dictionaries which contain stats for 
        # each user. 
        data = loadData()

    except ClientError:
        data = {}

    for i in range(50):
        response = requests.get('https://api.groupme.com/v3/groups/' + groupID + '/messages', params = requestParams)
        
        try:
            messages = response.json()['response']['messages']
        
        # The JSONDecodeError arises when there isn't enough messages in the group.
        except json.decoder.JSONDecodeError:
            break

        requestParams['before_id'] = messages[-1]['id']

        for message in messages:
            person = message['name']
           
            if person not in data:
                data[person] = {'messages':1, 'likes':len(message['favorited_by'])}
                    
            else:
                data[person]['messages'] += 1
                data[person]['likes'] += len(message['favorited_by'])

    return data


# Create a pandas DataFrame containing the data returned by getStats()
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


# Upload the new or updated leaderboard data to the AWS bucket and save a temporary copy of the leaderboard as a PNG in the ~/tmp file.
def saveNew(data):

