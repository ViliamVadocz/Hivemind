import socket

from messages import send_message, receive_message, INIT_MESSAGE, PACKET_MESSAGE


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
            send_message(INIT_MESSAGE, client)

            self.clients.append(client)

    def run(self):
        try:
            # Packet loop.
            while True:
                for client in self.clients:
                    print("[SERVER] Sending PACKET message")
                    send_message(PACKET_MESSAGE, client)
                    print("[SERVER] Receiving message")
                    message = receive_message(client)
                    self.parse_message(message)

        except Exception as e:
            print(e)
            print("[SERVER] Closing")
            self.socket.close()

    def parse_message(self, message):
        # TODO Parse message.
        pass


if __name__ == "__main__":
    test_server = Server(8085)
    test_server.listen_for_connections(1)
    test_server.run()
