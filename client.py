import socket
import time

print("\n\n\n")

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

class Client:
    def __init__(self, id):
        self.query1 = "query1"
        self.query2 = "query2"
        self.query3 = "query3"

        self.MESSAGE_404 = "DATA NOT FOUND"
        self.MESSAGE_200 = "OK"
        self.MESSAGE_401 = "UNAUTHORIZED"

        self.LENGTH_HEADER = 64
        self.CLIENT_ID_HEADER = 64
        self.STATUS_CODE_HEADER = 64
        self.RESPONSE_HEADER = 64
        self.MESSAGE_307_HEADER = 64
        self.status_code_response_HEADER = 64
        self.response_HEADER = 64

        self.CLIENT_MIDDLE_MAN_PORT = 5050
        self.SERVER = "192.168.86.25" # Local IP
        # self.SERVER = "162.229.185.98" # Global IP
        # self.SERVER = socket.gethostbyname(socket.gethostname()) # Local IP
        self.CLIENT_MIDDLE_MAN_ADDR = (self.SERVER, self.CLIENT_MIDDLE_MAN_PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.client_middle_man = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_middle_man.connect(self.CLIENT_MIDDLE_MAN_ADDR)

        self.connected = True

        self.id = id

    def handshake(self):
        time_syn = str(time.time()).encode(self.FORMAT)
        time_syn_length = str(len(time_syn)).encode(self.FORMAT)
        time_syn_length += b' ' * (self.LENGTH_HEADER - len(time_syn_length))

        confirmation = ("SYN").encode(self.FORMAT)
        confirmation_length = len(confirmation)
        send_confirmation_length = str(confirmation_length).encode(self.FORMAT)
        send_confirmation_length += b' ' * (self.LENGTH_HEADER - len(send_confirmation_length))

        self.client_middle_man.send(time_syn_length)
        self.client_middle_man.send(time_syn)
        self.client_middle_man.send(send_confirmation_length)
        self.client_middle_man.send(confirmation)

        while True:
            print("hello world!hello world!hello world!hello world!hello world!0000000")
            syn_ack_length = self.client_middle_man.recv(self.LENGTH_HEADER).decode(self.FORMAT)
            print("hello world!hello world!hello world!hello world!hello world!111111")
            if isint(syn_ack_length):
                print("hello world!hello world!hello world!hello world!hello world!222222")
                syn_ack_length = int(syn_ack_length)
                syn_ack = self.client_middle_man.recv(syn_ack_length).decode(self.FORMAT)
                print("hello world!hello world!hello world!hello world!hello world!333333")

                print("Handshake SYN ACK message from SERVER: ")
                print(syn_ack)

                ack = ("ACK").encode(self.FORMAT)
                ack_length = str(len(ack)).encode(self.FORMAT)
                ack_length += b' ' * (self.LENGTH_HEADER - len(ack_length))
                self.client_middle_man.send(ack_length)
                self.client_middle_man.send(ack)
                break


    def request(self, msg):
        time_start = str(time.time()).encode(self.FORMAT)
        time_start_length = str(len(time_start)).encode(self.FORMAT)
        time_start_length += b' ' * (self.LENGTH_HEADER - len(time_start_length))

        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.LENGTH_HEADER - len(send_length))
        id = str(self.id).encode(self.FORMAT)
        id += b' ' * (self.CLIENT_ID_HEADER - len(id))

        self.client_middle_man.send(id)
        self.client_middle_man.send(time_start_length)
        self.client_middle_man.send(time_start)
        self.client_middle_man.send(send_length)
        self.client_middle_man.send(message)
        print(f"\n\nQuery from CLIENT {self.id} to MIDDLE MAN:")
        print(msg)

def client_job(client):
    try:
        # client.handshake()
        client.request(client.query1)
        print("\n")
        print(f"[CLIENT {client.id}] QUERY SENT")
        print("\n")
        while client.connected:
            MESSAGE_307_length = client.client_middle_man.recv(client.MESSAGE_307_HEADER).decode(client.FORMAT)
            MESSAGE_307 = client.client_middle_man.recv(int(MESSAGE_307_length)).decode(client.FORMAT)

            status_code_response_length = client.client_middle_man.recv(client.status_code_response_HEADER).decode(client.FORMAT)
            status_code_response = client.client_middle_man.recv(int(status_code_response_length)).decode(client.FORMAT)

            if status_code_response == client.MESSAGE_200:
                response_length = client.client_middle_man.recv(client.response_HEADER).decode(client.FORMAT)
                response = client.client_middle_man.recv(int(response_length)).decode(client.FORMAT)

                print("Redirect Message: ")
                print(MESSAGE_307)
                print("Status code: ")
                print(status_code_response)
                print("\n")
                print("Response: ")
                print(response)
                client.connected = False
            else:
                print(status_code_response)
                client.connected = False

            # client.handshake()
    except:
        print(f"[CLIENT {client.id}] QUERY DENIED")

clients = [Client(i) for i in range(10)]
for i in range(len(clients)):
    client_job(clients[i])
    print("\n\n")

print("\n\n\n")
