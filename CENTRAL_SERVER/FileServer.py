import socket
import os

def main():
    StartServer()
        
def StartServer():
    IP = socket.gethostbyname(socket.gethostname())
    #IP = '10.61.3.218'
    PORT = 12346
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = 'utf-8'
    #SERVER_FOLDER = 'C:\\Users\\BioTech2070\\Documents\\BARNI\\FILE_SERVER\\slides'
    SERVER_FOLDER = 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\slides\\8808-04Ep'
    
    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print('[LISTENING] Server is listening.')
    
    while True:
        conn, addr = server.accept()
        print(f'[NEW CONNECTION] {addr} connected.\n')
        
        folder_name = conn.recv(SIZE).decode(FORMAT)
        
        path = os.path.join(os.getcwd(), folder_name)

        if os.path.isdir(path):
            return

        mrxs_name = folder_name + '.mrxs'
        
        #slides/folder_name/folder_name
        folder_path = os.path.join(SERVER_FOLDER, folder_name, folder_name)
        
        
        os.makedirs(folder_path)
        conn.send(f'Folder ({folder_name}) created.'.encode(FORMAT))

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
            
            if file_name == 'File transfer complete':
                conn.close()
                return
            
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