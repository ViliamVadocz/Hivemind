import socket

from messages import send_packet, receive_packet, INIT_MESSAGE, UPDATE_MESSAGE


class Server:

    def __init__(self, port):
        print("[SERVER] Loaded")
        # Create socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("localhost", port))
        self.clients = []

    def listen_for_connections(self, num_connections):
        # FIXME Might not work for >1.
        for _ in range(num_connections):
            self.socket.listen(1)
            print("[SERVER] Awaiting connection")
            client, address = self.socket.accept()
            print(f"[SERVER] Client connected from {address}")

            # Sends init message.
            send_packet(client, INIT_MESSAGE) 
            # TODO Wait for READY message.
            self.clients.append(client)


    def run(self):
        try:
            # Packet loop.
            while True:
                for client in self.clients:
                    print("[SERVER] Sending UPDATE message")
                    send_packet(client, UPDATE_MESSAGE)
                    print("[SERVER] Receiving packet")
                    message = receive_packet(client)
                    self.parse_packet(message)

        except Exception as e:
            print(e)
            print("[SERVER] Closing")
            self.socket.close()

    def parse_packet(self, message):
        # TODO Parse message.
        pass


if __name__ == "__main__":
    test_server = Server(23234)
    test_server.listen_for_connections(1)
    test_server.run()
