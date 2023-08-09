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
    
    #sending .mrxs file content
    #file = open(os.path.join(directoryName, directoryName), 'r')
    #file_data = file.read()
    #msg = f'{file_data}'
    #client.send(msg.encode(FORMAT))
    
    #server reply
    #msg = client.recv(SIZE).decode(FORMAT)
    #print(f'[SERVER] {msg}\n')
    
    #list files in directory
    path = os.path.join(directoryName, directoryName)
    files = sorted(os.listdir(path))
    
    for file_name in files:
        
        #sending .dat file names
        msg = f'FILENAME:{file_name}'
        print(f'[CLIENT] Sending file name: {file_name}')
        client.send(msg.encode(FORMAT))
        #server reply
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
        #sending .dat file data
        file = open(os.path.join(path, file_name), 'r', encoding='iso-8859-15')
        file_data = file.read()
        msg = f'DATA:{file_data}'
        client.send(msg.encode(FORMAT))
        #server reply
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
        #sending the close command
        msg = f'FINISH:Complete data send'
        client.send(msg.encode(FORMAT))
        #server reply
        msg = client.recv(SIZE).decode(FORMAT)
        print(f'[SERVER] {msg}\n')
        
    #closing connection from server
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