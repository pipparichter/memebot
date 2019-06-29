# Things to include in the leaderboard: total likes, total messages, likes per message.

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
def create():
    if boardExists(): # Update exsting board...
        
    else: 
        # This dictionary contains a every person in the groupchat who has sent a message in the last 1000 messages as keys
        # (or 10000 depending on how long the code takes to run). The values are also dictionaries which contain stats for 
        # each user. 
        people = {}
        for r in range(10):
            response = requests.get('https://api.groupme.com/v3', params = requestParams).json()
            requestParams['before_id'] = response[]


# Upload the updated leaderboard to the AWS bucket.
# def saveNew():
