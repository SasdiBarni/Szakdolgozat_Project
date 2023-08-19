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
        file = open(file_path, 'w')        
        
        
        while True:
            
            file_name = conn.recv(SIZE).decode(FORMAT)
            print(f'[CLIENT] Recived the filename: {file_name}.')
            conn.send('Filename recived.'.encode(FORMAT))
            
            file_size = conn.recv(SIZE).decode(FORMAT)
            print(f'[CLIENT] Recived the filesize: {file_size}.')
            conn.send('Filesize recived.'.encode(FORMAT))
            
            file_path = os.path.join(folder_path, file_name)
            file = open(file_path, 'w', encoding='iso-8859-15')
            
            file_bytes = f''
            
            while True:
                print(f'[CLIENT] Recieving the file data...')
                file_data = conn.recv(SIZE).decode('iso-8859-15')
                if file_data[-5:] == f'<END>':
                    file_data = file_data[:len(file_data) - 5]
                    file_bytes += file_data
                    break
                else:
                    file_bytes += file_data
            
            file.write(file_bytes)
            conn.send('File data recived and saved.'.encode(FORMAT))
            file.close()
            
        
    
if __name__ == '__main__':
    main()