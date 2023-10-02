import socket               # Import socket module
import os
#import paramiko


def SendToFileServer(directoryName):
    SIZE = 1024
    FORMAT = 'utf-8'
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    #send directoryName
    msg = f'{directoryName}'
    print(f'[CLIENT] Sending folder name: {directoryName}')
    client.send(msg.encode(FORMAT))
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    
    #sending .mrxs file content
    file = open(os.path.join(directoryName, directoryName + '.mrxs'), 'rb')
    file_data = file.read()
    print('[CLIENT] Sending .mrxs file data...')
    client.sendall(file_data)
    client.send(b'<END>')
    file.close()
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    
    
    #list files in directory
    path = os.path.join(directoryName, directoryName)
    files = sorted(os.listdir(path))
    
    
    for file_name in files:
        
        file = open(os.path.join(path, file_name), 'rb')
        file_size = os.path.getsize(os.path.join(path, file_name))
        
        msg = f'{file_name}'
        print(f'[CLIENT] Sending file name: {file_name}')
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
        print(f'[CLIENT] Sending file size: {file_size}')
        client.send(str(file_size).encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
        data = file.read()
        print('[CLIENT] Sending file data...')
        client.sendall(data)
        client.send(b'<END>')
        file.close()
        
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
        
    msg = f'File transfer complete'
    client.send(msg.encode(FORMAT))
    client.close()
    return
    
    
def SendToCentralServer(date, user, jobID, directoryName):
    SIZE = 1024
    FORMAT = 'utf-8'
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    toSend = str(date) + ';' + str(user) + ';' + str(jobID) + ';' + str(directoryName)    
    client.sendall(toSend.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER]: {msg}')
    
    msg = 'Disconnected.'
    client.send(msg.encode(FORMAT))
    client.close()

'''
def GetResultsFromServer():    
    SSH_Client= paramiko.SSHClient()
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH_Client.connect( 
                    hostname = 'hostName', 
                    port = 4455, 
                    username = 'userName',
                    password = 'password', 
                    look_for_keys = False
                )
    
    sftp_client = SSH_Client.open_sftp()
    results = sftp_client.listdir('media\\nfs\\results')
    
    for result in results :
        sftp_client.get(f'media\\nfs\\results\\{str(result)}', os.getcwd())
        
    sftp_client.close()

def GetFilesFromServer():
    SSH_Client= paramiko.SSHClient()
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH_Client.connect( 
                    hostname = 'hostName', 
                    port = 4455, 
                    username = 'userName',
                    password = 'password', 
                    look_for_keys = False
                )
    
    sftp_client = SSH_Client.open_sftp()
    slides = sftp_client.listdir('media\\nfs\\slides')
    
    return slides
    
'''