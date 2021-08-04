import socket
import time

print("\n\n\n")

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

class Server():
    client_frequencies = {}
    def __init__(self, id):
        self.id = id

        self.response = ""
        self.response_length = 0
        self.status_code = ""
        self.status_code_length = 0

        self.MESSAGE_404 = "DATA NOT FOUND"
        self.MESSAGE_200 = "OK"
        self.MESSAGE_401 = "UNAUTHORIZED"

        self.query1 = "query1"
        self.query2 = "query2"
        self.query3 = "query3"

        self.response1 = "response1"
        self.response2 = "response2"
        self.response3 = "response3"

        self.LENGTH_HEADER = 64
        self.CLIENT_ID_HEADER = 64
        self.SERVER_ID_HEADER = 64
        self.STATUS_CODE_HEADER = 64
        self.RESPONSE_HEADER = 64

        self.SERVER = "192.168.86.25"  # Local IP
        # self.SERVER = "162.229.185.98" # Global IP
        # self.SERVER = socket.gethostbyname(socket.gethostname()) # Local IP
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.MIDDLE_MAN_SERVER_PORT = 8000
        self.MIDDLE_MAN_SERVER_ADDR = (self.SERVER, self.MIDDLE_MAN_SERVER_PORT)

        self.middle_man_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.middle_man_server.bind(self.MIDDLE_MAN_SERVER_ADDR)
        self.conn_middle_man = None

        self.connected = True

    def handshake(self, handshake):
        while True:
            print("hello world!hello world!hello world!hello world!hello world!111111")
            time_syn_length = self.conn_middle_man.recv(self.LENGTH_HEADER).decode(self.FORMAT)
            print("hello world!hello world!hello world!hello world!hello world!222222")
            if isint(time_syn_length):
                time_syn_length = int(time_syn_length)
                print("hello world!hello world!hello world!hello world!hello world!33333")
                time_syn = float(self.conn_middle_man.recv(time_syn_length))
                print("hello world!hello world!hello world!hello world!hello world!44444")
                confirmation_length = self.conn_middle_man.recv(self.LENGTH_HEADER).decode(self.FORMAT)
                print("hello world!hello world!hello world!hello world!hello world!5555555")
                confirmation_length = int(confirmation_length)
                print("hello world!hello world!hello world!hello world!hello world!66666666")
                confirmation = self.conn_middle_man.recv(confirmation_length).decode(self.FORMAT)

                if handshake:
                    print("Handshake SYN message from CLIENT: ")
                    print(confirmation)

                syn_ack = ("SYN ACK").encode(self.FORMAT)
                syn_ack_length = str(len(syn_ack)).encode(self.FORMAT)
                syn_ack_length += b' ' * (self.LENGTH_HEADER - len(syn_ack_length))

                self.conn_middle_man.send(syn_ack_length)
                self.conn_middle_man.send(syn_ack)

                ack_length = self.conn_middle_man.recv(self.LENGTH_HEADER).decode(self.FORMAT)
                if isint(ack_length):
                    ack_length = int(ack_length)
                    ack = self.conn_middle_man.recv(ack_length).decode(self.FORMAT)
                    time_ack = time.time()

                    if handshake:
                        print("Handshake ACK from CLIENT: ")
                        print(ack)

                        print("\n\n")
                        print("Handshake time (secs): " + str(time_ack - time_syn))
                    else:
                        return time_syn

                    break

    def respond(self, client_id, msg):
        if msg == self.query1:
            self.response = self.response1
            self.status_code = self.MESSAGE_200
        elif msg == self.query2:
            self.response = self.response2
            self.status_code = self.MESSAGE_200
        elif msg == self.query3:
            self.response = self.response3
            self.status_code = self.MESSAGE_200
        else:
            self.status_code = self.MESSAGE_404

        self.id_send = str(self.id).encode(self.FORMAT)
        self.id_send += b' ' * (self.SERVER_ID_HEADER - len(self.id_send))
        self.conn_middle_man.send(self.id_send)

        self.status_code = self.status_code.encode(self.FORMAT)
        self.status_code_length = str(len(self.status_code)).encode(self.FORMAT)
        self.status_code_length += b' ' * (self.STATUS_CODE_HEADER - len(self.status_code_length))
        self.conn_middle_man.send(self.status_code_length)
        self.conn_middle_man.send(self.status_code)

        print(f"Response to CLIENT {client_id} to SERVER {self.id}:")
        print(self.response)
        self.response = self.response.encode(self.FORMAT)
        self.response_length = str(len(self.response)).encode(self.FORMAT)
        self.response_length += b' ' * (self.RESPONSE_HEADER - len(self.response_length))
        self.conn_middle_man.send(self.response_length)
        self.conn_middle_man.send(self.response)


def server_job(server):
    try:
        server.middle_man_server.listen()
        server.conn_middle_man, addr = server.middle_man_server.accept()
        while server.connected:
            # server.handshake(True)
            client_id = server.conn_middle_man.recv(server.CLIENT_ID_HEADER).decode(server.FORMAT)
            if isint(client_id):
                client_id = int(client_id)
                time_start_length = server.conn_middle_man.recv(server.LENGTH_HEADER).decode(server.FORMAT)
                time_start = float(server.conn_middle_man.recv(int(time_start_length)).decode(server.FORMAT))
                query_length = server.conn_middle_man.recv(server.LENGTH_HEADER).decode(server.FORMAT)
                query = str(server.conn_middle_man.recv(int(query_length)).decode(server.FORMAT))

                time_intermediate = time.time()

                print(f"\n\nQuery from CLIENT {client_id} to SERVER {server.id}:")
                print(query)
                print("\n")

                print("Time taken to receive query from client (secs): " + str(time_intermediate - time_start))

                server.respond(client_id, query)

                # server.connected = False
            # time_end = server.handshake(False)
            print("\n\n")
            print("Time taken to receive respond to client (secs): " + str(time_end - time_intermediate) + "\n")
            print("Total time taken (secs): " + str(time_end - time_start))
    except:
        print("COULD NOT CONNECT")

server = Server(0)
server_job(server)
print("\n\n\n")