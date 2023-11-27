import socket               # Import socket module
import os
import pathlib

def SendToFileServer(directoryName):
    SIZE = 1024
    FORMAT = 'utf-8'
    IP = '10.61.3.218'
    PORT = 12346
    ADDR = (IP, PORT)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    
    #send directoryName
    msg = f'{directoryName}'
    print(f'[CLIENT] Sending folder name: {directoryName}')
    client.send(msg.encode(FORMAT))
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    
    #sending .mrxs file content
    path = os.path.join(pathlib.Path(__file__).parent.resolve(), directoryName + '\\' + directoryName + '.mrxs')
    file = open(path, 'rb')
    file_data = file.read()
    print('[CLIENT] Sending .mrxs file data...')
    client.sendall(file_data)
    client.send(b'<END>')
    file.close()
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    
    #list files in directory
    path = os.path.join(pathlib.Path(__file__).parent.resolve(), directoryName + '\\' + directoryName)
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
    IP=socket.gethostbyname(socket.gethostname())
    #IP = '10.61.3.218'
    PORT = 12345
    ADDR = (IP, PORT)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))
    
    
    toSend = str(date) + ';' + str(user) + ';' + str(jobID) + ';' + str(directoryName)    
    client.sendall(toSend.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER]: {msg}')
    
    msg = 'Disconnected.'
    client.send(msg.encode(FORMAT))
    
    msg = client.recv(SIZE).decode(FORMAT)
    
    client.close()