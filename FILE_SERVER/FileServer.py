import socket
import os

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
        file = open(file_path, 'wb')
        
        i = 0
        
        while True:
            
            if i == 0:
                file_bytes = b''
            
                done = False
                x = 0
        
                while not done:
                    x += 1
                    if file_bytes[-5:] == b'<END>':
                        file_bytes = file_bytes[:len(file_bytes) - 5]
                        done = True
                    else:
                        file_data = conn.recv(SIZE)
                        file_bytes += file_data
            
                i = 1
                file.write(file_bytes)
                print(f'[SERVER] .mrxs file data recived and saved.\n')
                conn.send('.mrxs file data recived and saved.'.encode(FORMAT))
                file.close()        
            
            file_name = conn.recv(SIZE).decode(FORMAT)
            print(f'[CLIENT] Recived the filename: {file_name}.')
            conn.send('Filename recived.'.encode(FORMAT))
            
            file_size = conn.recv(SIZE).decode(FORMAT)
            print(f'[CLIENT] Recived the filesize: {file_size}.')
            conn.send('Filesize recived.'.encode(FORMAT))
            
            file_path = os.path.join(folder_path, file_name)
            file = open(file_path, 'wb')
            
            file_bytes = b''
            
            done = False
            x = 0
                        
            while not done:
                x += 1
                if file_bytes[-5:] == b'<END>':
                    file_bytes = file_bytes[:len(file_bytes) - 5]
                    done = True
                else:
                    file_data = conn.recv(SIZE)
                    file_bytes += file_data
            
            file.write(file_bytes)
            print(f'[SERVER] File data recived and saved.\n')
            conn.send('File data recived and saved.'.encode(FORMAT))
            file.close()
            
        
    
if __name__ == '__main__':
    main()