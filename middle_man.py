import socket
import time
import threading

print("\n\n\n")

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

class MiddleMan():
    def __init__(self):
        self.MESSAGE_307 = ""
        self.MESSAGE_307_length = None
        self.status_code_response = ""
        self.status_code_response_length = None
        self.response = ""
        self.response_length = None

        self.query1 = "query1"
        self.query2 = "query2"
        self.query3 = "query3"

        self.response1 = "response1"
        self.response2 = "response2"
        self.response3 = "response3"

        self.MESSAGE_404 = "DATA NOT FOUND"
        self.MESSAGE_200 = "OK"
        self.MESSAGE_401 = "UNAUTHORIZED"

        self.LENGTH_HEADER = 64
        self.CLIENT_ID_HEADER = 64
        self.STATUS_CODE_HEADER = 64
        self.RESPONSE_HEADER = 64
        self.SERVER_ID_HEADER = 64
        self.MESSAGE_307_HEADER = 64
        self.status_code_response_HEADER = 64
        self.response_HEADER = 64

        self.CLIENT_MIDDLE_MAN_PORT = 5050
        self.SERVER = "192.168.86.25"  # Local IP
        # self.SERVER = "162.229.185.98" # Global IP
        # self.SERVER = socket.gethostbyname(socket.gethostname()) # Local IP
        self.CLIENT_MIDDLE_MAN_ADDR = (self.SERVER, self.CLIENT_MIDDLE_MAN_PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.client_middle_man = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_middle_man.bind(self.CLIENT_MIDDLE_MAN_ADDR)
        self.conn_client = None


        self.MIDDLE_MAN_SERVER_PORT = 8000
        self.MIDDLE_MAN_SERVER_ADDR = (self.SERVER, self.MIDDLE_MAN_SERVER_PORT)

        self.middle_man_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.middle_man_server.connect(self.MIDDLE_MAN_SERVER_ADDR)

        self.connected = True

    def handshake(self):
        while True:
            print("hello world!hello world!hello world!hello world!hello world!111111")
            time_syn_length = self.conn_client.recv(self.LENGTH_HEADER).decode(self.FORMAT)
            print(isint(time_syn_length), time_syn_length)
            print("hello world!hello world!hello world!hello world!hello world!222222")
            if isint(time_syn_length):
                print("hello world!hello world!hello world!hello world!hello world!33333")
                time_syn_length = int(time_syn_length)
                print("hello world!hello world!hello world!hello world!hello world!4444")
                time_syn = self.conn_client.recv(time_syn_length)
                print("hello world!hello world!hello world!hello world!hello world!5555")
                confirmation_length = self.conn_client.recv(self.LENGTH_HEADER).decode(self.FORMAT)
                print("hello world!hello world!hello world!hello world!hello world!66666")
                confirmation_length = int(confirmation_length)
                print("hello world!hello world!hello world!hello world!hello world!777777")
                confirmation = self.conn_client.recv(confirmation_length).decode(self.FORMAT)
                print("Handshake SYN message from CLIENT: ")
                print(confirmation)

                time_syn_length = str(time_syn_length).encode(self.FORMAT)
                time_syn_length += b' ' * (self.LENGTH_HEADER - len(time_syn_length))
                confirmation_length = str(confirmation_length).encode(self.FORMAT)
                confirmation_length += b' ' * (self.LENGTH_HEADER - len(confirmation_length))
                confirmation = confirmation.encode(self.FORMAT)

                self.middle_man_server.send(time_syn_length)
                self.middle_man_server.send(time_syn)
                self.middle_man_server.send(confirmation_length)
                self.middle_man_server.send(confirmation)

                syn_ack_length = self.middle_man_server.recv(self.LENGTH_HEADER).decode(self.FORMAT)
                if isint(syn_ack_length):
                    syn_ack_length = int(syn_ack_length)
                    syn_ack = self.middle_man_server.recv(syn_ack_length).decode(self.FORMAT)
                    print("Handshake SYN ACK from SERVER: ")
                    print(syn_ack)

                    syn_ack_length = str(syn_ack_length).encode(self.FORMAT)
                    syn_ack_length += b' ' * (self.LENGTH_HEADER - len(syn_ack_length))
                    syn_ack = syn_ack.encode(self.FORMAT)
                    self.conn_client.send(syn_ack_length)
                    self.conn_client.send(syn_ack)

                    ack_length = self.conn_client.recv(self.LENGTH_HEADER).decode(self.FORMAT)
                    if isint(ack_length):
                        ack_length = int(ack_length)
                        ack = self.conn_client.recv(ack_length).decode(self.FORMAT)

                        print("Handshake ACK from CLIENT: ")
                        print(ack)

                        ack_length = str(ack_length).encode(self.FORMAT)
                        ack_length += b' ' * (self.LENGTH_HEADER - len(ack_length))
                        ack = ack.encode(self.FORMAT)
                        self.middle_man_server.send(ack_length)
                        self.middle_man_server.send(ack)

                        break





    def request_server(self, client_id, msg, time_start):
        time_start = time_start.encode(self.FORMAT)
        time_start_length = len(time_start)
        time_start_length = str(time_start_length).encode(self.FORMAT)
        time_start_length += b' ' * (self.LENGTH_HEADER - len(time_start_length))

        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.LENGTH_HEADER - len(send_length))
        id = str(client_id).encode(self.FORMAT)
        id += b' ' * (self.CLIENT_ID_HEADER - len(id))

        self.middle_man_server.send(id)
        self.middle_man_server.send(time_start_length)
        self.middle_man_server.send(time_start)
        self.middle_man_server.send(send_length)
        self.middle_man_server.send(message)

    def respond_client(self, client_id, server_id, status_code, response):
        self.MESSAGE_307 = "[CLIENT] " + str(client_id) + " TEMPORARY REDIRECT TO SERVER " + str(server_id)
        self.MESSAGE_307 = self.MESSAGE_307.encode(self.FORMAT)
        self.MESSAGE_307_length = str(len(self.MESSAGE_307)).encode(self.FORMAT)
        self.MESSAGE_307_length += b' ' * (self.MESSAGE_307_HEADER - len(self.MESSAGE_307_length))
        self.conn_client.send(self.MESSAGE_307_length)
        self.conn_client.send(self.MESSAGE_307)

        self.status_code_response = status_code
        self.status_code_response = self.status_code_response.encode(self.FORMAT)
        self.status_code_response_length = str(len(self.status_code_response)).encode(self.FORMAT)
        self.status_code_response_length += b' ' * (self.status_code_response_HEADER - len(self.status_code_response_length))
        self.conn_client.send(self.status_code_response_length)
        self.conn_client.send(self.status_code_response)

        if status_code == self.MESSAGE_200:
            self.response = response
            self.response = self.response.encode(self.FORMAT)
            self.response_length = str(len(self.response)).encode(self.FORMAT)
            self.response_length += b' ' * (self.response_HEADER - len(self.response_length))
            self.conn_client.send(self.response_length)
            self.conn_client.send(self.response)



def middle_man_job(middle_man):
    try:
        while middle_man.connected:
            # middle_man.handshake()
            client_id = middle_man.conn_client.recv(middle_man.CLIENT_ID_HEADER).decode(middle_man.FORMAT)
            if isint(client_id):
                client_id = int(client_id)
                time_start_length = middle_man.conn_client.recv(middle_man.LENGTH_HEADER).decode(middle_man.FORMAT)
                time_start = str(middle_man.conn_client.recv(int(time_start_length)).decode(middle_man.FORMAT))
                query_length = middle_man.conn_client.recv(middle_man.LENGTH_HEADER).decode(middle_man.FORMAT)
                query = str(middle_man.conn_client.recv(int(query_length)).decode(middle_man.FORMAT))

                middle_man.request_server(client_id, query, time_start)

                server_id = (middle_man.middle_man_server.recv(middle_man.SERVER_ID_HEADER)).decode(middle_man.FORMAT)
                server_id = int(server_id)

                print(f"\n\nQuery from CLIENT {client_id} to SERVER {server_id}: ")
                print(query)

                status_code_length = middle_man.middle_man_server.recv(middle_man.status_code_response_HEADER).decode(middle_man.FORMAT)
                status_code = middle_man.middle_man_server.recv(int(status_code_length)).decode(middle_man.FORMAT)
                response_length = middle_man.middle_man_server.recv(middle_man.response_HEADER).decode(middle_man.FORMAT)
                response = middle_man.middle_man_server.recv(int(response_length)).decode(middle_man.FORMAT)

                print("\n")
                print(f"Response from SERVER {server_id} to CLIENT {client_id}: ")
                print(response)

                middle_man.respond_client(client_id, server_id, status_code, response)



                # middle_man.connected = False
            # middle_man.handshake()
    except:
        print("COULD NOT CONNECT")

middle_man = MiddleMan()
middle_man.client_middle_man.listen()
while True:
    conn, addr = middle_man.client_middle_man.accept()
    middle_man.conn_client = conn
    thread = threading.Thread(target=middle_man_job, args=(middle_man,))
    thread.start()
