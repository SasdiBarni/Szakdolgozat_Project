import SlideApplication
import FileServer
import socket


def main():
    
    data = StartServer().split(';')
    
    Date = data[0]
    User = data[1]
    JobID = data[2]
    directoryName = data[3]
    
    FileServer.main()
            
    SlideApplication.OpenSlide(SlideApplication.ssi, directoryName, JobID)

def StartServer():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4456
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = 'utf-8'
    
    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print('[LISTENING] Server is listening.')
    
    while True:
        conn, addr = server.accept()
        print(f'[NEW CONNECTION] -{addr}- has been connected.')
        
        data = conn.recv(SIZE).decode(FORMAT)
        print(f'[RECIVED] {str(data)} has been recived.')
        conn.send('Data has been recived succesfully.'.encode(FORMAT))
        
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f'[CLIENT] {addr} {msg}\n')
        conn.close()
        return data
        

if __name__ == '__main__':
    main()