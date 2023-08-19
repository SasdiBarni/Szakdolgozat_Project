import socket               # Import socket module
import os


def SendToFileServer(directoryName):
    SIZE = 1024
    FORMAT = 'utf-8'
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    
    #connect to FileServer
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    #send directoryName
    msg = f'{directoryName}'
    print(f'[CLIENT] Sending folder name: {directoryName}')
    client.send(msg.encode(FORMAT))
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    
    """
    #sending .mrxs file content
    file = open(os.path.join(directoryName, directoryName), 'r')
    file_data = file.read()
    msg = f'{file_data}'
    client.sendall(msg.encode(FORMAT))
    
    #server reply
    msg = client.recv(SIZE).decode(FORMAT)
    print(f'[SERVER] {msg}\n')
    """
    
    #list files in directory
    path = os.path.join(directoryName, directoryName)
    files = sorted(os.listdir(path))
    
    
    for file_name in files:
        
        file = open(os.path.join(path, file_name), 'r', encoding='iso-8859-15')
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
        client.sendall(data.encode('iso-8859-15'))
        client.send('<END>'.encode('iso-8859-15'))
        
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        file.close()
        
        
    msg = f'CLOSE:File transfer is completed'
    client.send(msg.encode(FORMAT))
    client.close()
    
    
def SendToCentralServer(date, user, jobID, directoryName):
    SIZE = 1024
    FORMAT = 'utf-8'
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4456
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