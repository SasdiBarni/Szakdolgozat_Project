import json

def LoginAuthenticate(username, pw):
    
    f = open('users.json')

    data = json.load(f)
    
    for i in data['users']:
        if username == i['username'] and pw == i['pw']:
            return True
        else:
            continue
