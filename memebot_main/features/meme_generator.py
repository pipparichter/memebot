import sys
sys.path.append('../dictionaries')
sys.path.append('..')

import meme_dict as memes
import bot_reply

import random

# This function contains the procedure needed for the user to specify a category of meme, to be sent into the designated group chat. 
def memeGenerator():
  
    categories = [key for key in memes.memeDict.keys()]
  
    bot_reply.sendMessage('heck ya, what category of meme? (nerdy, wholesome, inside jokes)')
  
    reply = bot_reply.readReply()
  
    if reply == 0:
            return 'oops, your meme request timed out. get it together and try again.'
    else:
        if reply in categories:
            memeList = memes.memeDict[reply]
            return random.choice(memeList)
        else:
            return 'oops, you didn\'t respond with a valid category of meme. get it together and try again.'

