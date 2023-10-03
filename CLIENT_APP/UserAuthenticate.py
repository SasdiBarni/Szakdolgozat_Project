import json
import os

def LoginAuthenticate(username, pw):
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
    
    f = open(path)

    data = json.load(f)
    
    for i in data['users']:
        if username == i['username'] and pw == i['pw']:
            return True
        else:
            return False
