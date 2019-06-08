import requests

token = 'J4pPmVtQuGb3wDCKQFXSFkATcdwXMUNPjFV6LIdM'


# Takes the path to an image (jpeg or png) in local memory, and returns a URL (as a string) from the GroupMe Image Service which can be posted to GroupMe
# via the GroupMe API.
def picToURL(pathString):
    headers = {'X-Access-Token':token,'Content-Type': 'image/jpeg'}
    
    # If, for whatever reason, you forget how the with statement works, check out this link: https://effbot.org/zone/python-with-statement.htm.
    with open(pathString, 'rb') as image:
        binaryImage = image.read()

    
    response = requests.post('https://image.groupme.com/pictures', data = binaryImage, headers = headers, params = {'access_token':token})
    
    return response.json()['payload']['picture_url'] + '.large'
    
    
##########################################################################################################################################################

keepGoing = True        

print('I see you want to convert an image to a GroupMe URL... well you\'ve come to the right place.\n')


# The user can input either a single path or several paths separated by ', ', and prints each corresponding postable URL in series.
while keepGoing:          
    cont = input('Do you want to convert an image? (Y/N): ')
    if cont == 'Y':
        while True:
            try:    
                pathStrings = input('Paste the image path(s) here: ').split(', ')    
                print('Here are your link(s): ')
                for string in pathStrings:
                    print(picToURL(string))
                break
            except FileNotFoundError:
                print('Not a valid file. Try again.')
                break    
    elif cont == 'N':
        keepGoing = False
    else:
        print('Seriously, it\'s not that hard, choose Y or N.' + '\n')
               
    
print('\n' + 'Bye bitch.')
    

    
    









