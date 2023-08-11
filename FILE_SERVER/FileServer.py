import socket
import os
import sys

def main():
    StartServer()
        
def StartServer():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = 'utf-8'
    SERVER_FOLDER = 'slides'
    
    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print('[LISTENING] Server is listening.')
    
    while True:
        conn, addr = server.accept()
        print(f'[NEW CONNECTION] {addr} connected.')
        
        folder_name = conn.recv(SIZE).decode(FORMAT)
        
        mrxs_name = folder_name + '.mrxs'
        
        #slides/folder_name/folder_name
        folder_path = os.path.join(SERVER_FOLDER, folder_name, folder_name)
        
        #creting the folders if not existing
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            conn.send(f'Folder ({folder_name}) created.'.encode(FORMAT))
        else:
            conn.send(f'Folder ({folder_name}) already exists.'.encode(FORMAT))

        file_path = os.path.join(SERVER_FOLDER, folder_name, mrxs_name)
        file = open(file_path, 'w')
        
        CHUNK_SIZE = 8 * 1024

        chunk = server.recv(CHUNK_SIZE)
        while chunk:
            chunk = server.recv(CHUNK_SIZE)
            file = open(file_path, 'w', encoding='iso-8859-15')
            file.write(chunk)
        server.close()
        
        """
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f'[CLIENT] Recieving the file data.')
        file.write(msg)
        conn.send('File data recived.'.encode(FORMAT))
        """
        
        """
        i = 0
        
        isFileName = True

        while True:
            
            if isFileName:
                msg = conn.recv(SIZE).decode(FORMAT)
                cmd, data = msg.split(':')
                isFileName = False
                i = 0
            else:
                msg = conn.recv(SIZE).decode('iso-8859-15')
                if i == 0:                    
                    cmd, data = msg.split('::')
                else:
                    print(str(msg))
                    if 'FINISH:Complete data send' in msg:
                        cmd, data = msg.split(':')
                    else:
                        cmd = 'DATA'
                        data = msg
            
            #recive .dat filenames
            if cmd == 'FILENAME':
                print(f'[CLIENT] Recived the filename: {data}.')
                file_path = os.path.join(folder_path, data)
                file = open(file_path, 'w', encoding='iso-8859-15')
                conn.send('Filename recived.'.encode(FORMAT))
            
            #recive .dat file data
            elif cmd == 'DATA':
                i = 1
                print(f'[CLIENT] Recieving the file data.')
                file.write(data)
                conn.send('File data recived.'.encode(FORMAT))
            
            elif cmd == 'FINISH':
                file.close()
                print(f'[CLIENT] {data}.\n')
                conn.send('The data is saved.'.encode(FORMAT))
            
            elif cmd == 'CLOSE':
                conn.close()
                print(f'[CLIENT] {data}')
                break
        """
    
if __name__ == '__main__':
    main()