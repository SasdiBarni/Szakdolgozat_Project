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
        
        #msg = conn.recv(SIZE).decode(FORMAT)
        #print(f'[CLIENT] Recieving the file data.')
        #file.write(msg)
        #conn.send('File data recived.'.encode(FORMAT))
       
        i = 2

        while True:
            
            if i % 2 == 0:
                msg = conn.recv(SIZE).decode(FORMAT)
                cmd, data = msg.split(':')
                i += 1
            else:
                msg = conn.recv(SIZE).decode(FORMAT)
                cmd, data = msg.split(':')
            
            #recive .dat filenames
            if cmd == 'FILENAME':
                print(f'[CLIENT] Recived the filename: {data}.')
                file_path = os.path.join(folder_path, data)
                file = open(file_path, 'w')
                conn.send('Filename recived.'.encode(FORMAT))
            
            #recive .dat file data
            elif cmd == 'DATA':
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

    
if __name__ == '__main__':
    main()