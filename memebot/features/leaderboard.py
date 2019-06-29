# Things to include in the leaderboard: total likes, total messages, likes per message, messages liked(?).

import sys
sys.path.append('../')

import requests 
import pandas as pd

# import boto3
# s3 = boto3.client('s3')

import bot_reply
import global_vars

token = global_vars.token
groupID = global_vars.groupID

bucketName = 'gm-memebot'

requestParams = {'token':token, 'group_id':groupID, 'limit':100}


# Check to see if a leaderboard is already saved in the AWS bucket.
# def boardExists():
    

# If a leaderboard exists, update it. If not, create a new leaderboard.
def getStats():
    if ! boardExists():  
        # This dictionary contains a every person in the groupchat who has sent a message in the last 1000 messages as keys
        # (or 10000 depending on how long the code takes to run). The values are also dictionaries which contain stats for 
        # each user. 
        data = {}

    else: # Update existing board...

    for i in range(10):
        messages = requests.get('https://api.groupme.com/v3', params = requestParams).json()['messages']
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
def leaderboard():


# Upload the updated leaderboard to the AWS bucket.
# def saveNew():
