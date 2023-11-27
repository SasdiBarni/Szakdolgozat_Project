import SlideApplication
import FileServer
import socket


def main():
    print('VERSION 2.0')
    data = StartServer().split(';')
    
    Date = data[0]
    User = data[1]
    JobID = data[2]
    directoryName = data[3]

    #FileServer.main()

    SlideApplication.OpenSlide(directoryName, JobID, Date, User)

    main()

def StartServer():
    IP=socket.gethostbyname(socket.gethostname())
    #IP = '10.61.3.218'
    PORT = 12345
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = 'utf-8'
    
    print('[STARTING] Server is starting.')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
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