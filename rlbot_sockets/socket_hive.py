import socket

from messages import send_message, receive_message, READY_MESSAGE, INPUT_MESSAGE


class SocketHivemind:

    def __init__(self, port):
        print("[HIVEMIND] Loaded")
        # Create socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[HIVEMIND] Attempting to connect")
        self.socket.connect(("localhost", port))
        print("[HIVEMIND] Connected")
        print("[HIVEMIND] Sending READY message")
        send_message(READY_MESSAGE, self.socket)

    def run(self):
        try:
            # Packet loop.
            while True:
                print("[HIVEMIND] Receiving message")
                message = receive_message(self.socket)
                self.parse_message(message)

        except Exception as e:
            print(e)
            print("[HIVEMIND] Closing")
            self.socket.close()

    def parse_message(self, message):
        # TODO Parse message
        # E.g. if the message is of type "Update", call get_output.
        self.get_output(message)

    def get_output(self, message):
        print("[HIVEMIND] Sending INPUT message")
        send_message(INPUT_MESSAGE, self.socket)

if __name__ == "__main__":
    hivemind = SocketHivemind(8085)
    hivemind.run()

