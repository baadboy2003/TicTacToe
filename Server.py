import socket
import threading
##########################socket#################
HEADER = 64
PORT = 1000
SERVER = socket.gethostbyname(socket.gethostname())  # Get the IP address from the system
ADDR = (SERVER, PORT)  #this is ADDR is used to put the server and port tgt so we dont have to constly type them seperately
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "D" ### basicly when the signal from client is recevied we discconet 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) # basicly binds or another words starts the server in ADDR

active_connections = 0 #At the begining alwys the connections will be zero
active_connections_lock = threading.Lock() # so basiclly when I tried connecting and disconnecting the active users keep coming out wrong that is beacuse of the thread issue that is why must use lock to share between 2 threads

def send_message_to_client(conn, message):
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def handle_client(conn, addr):
    global active_connections
    print(f"[NEW CONNECTION] {addr} connected.")
    #send_message_to_client(conn,"hello client1")
    
    with active_connections_lock:
        active_connections += 1
        print(f"[ACTIVE CONNECTIONS] {active_connections}")
    


    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

    with active_connections_lock:
        active_connections -= 1
        print(f"[ACTIVE CONNECTIONS] {active_connections}")

    conn.close()

def start_server():
    server.listen() ###this is the most important one with the help of this you actually start the server 
    while True:
        conn, addr = server.accept() #this will accept the client ip and port
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print(f"Server has started @ {SERVER}")
start_server()
