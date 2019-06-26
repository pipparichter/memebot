from wsgiref.simple_server import make_server
import cgi

import requests
import time
import os
import sys
import json

sys.path.append('./memebot/features')
sys.path.append('./memebot/dictionaries')
sys.path.append('./memebot')

import global_vars
import bot_reply


token = global_vars.token
groupID = global_vars.groupID
botID = global_vars.botID

requestParams = {'token':token, 'limit':1}


def app(environ, startResponse):
    try:
        requestBodySize = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        requestBodySize = 0
        
    # message = json.loads(environ['wsgi.input'].read(requestBodySize).decode('utf-8'))
    print(environ['wsgi.input'].read(requestBodySize).decode('utf-8'))
    messageText = message['text']
    
    if (messageText in bot_reply.staticTriggers) or (messageText in bot_reply.dynamicTriggers):
        bot_reply.botReply(message)

    responseBody = bytes(messageText, 'utf-8') 
       
    status = '200 OK'
    responseHeaders = [('Content-Type', 'text/plain'), ('Content-Length', str(len(responseBody)))]

    startResponse(status, responseHeaders)

    return [responseBody]


# port = int(os.environ.get('PORT'))
# print(port)

# server = make_server('https://gm-memebot.herokuapp.com', port, app)
# server = make_server('gm-memebot.herokuapp.com', 810, app)

# print(os.environ['PORT'])

# server.serve_forever()
