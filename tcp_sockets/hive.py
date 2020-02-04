import socket

from messages import send_packet, receive_packet, INPUT_MESSAGE

ID = 0
NUM_BOTS = 4

# notice: multiplicity == 4, telling RLBot I want to control bots.
# controlled ids are [id, id + 1, id + 2, id + 3]
# There must be enough cars in the match config file to support this.
HIVE_READY_MESSAGE = {
    "type": "Ready",
    "name": "Hivemind",
    "team": 0,
    "id": ID,
    "multiplicity": NUM_BOTS
}


class SocketHivemind:

    def __init__(self, port):
        print("[HIVEMIND] Loaded")
        # Create socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[HIVEMIND] Attempting to connect")
        self.socket.connect(("localhost", port))
        print("[HIVEMIND] Connected")
        print("[HIVEMIND] Sending READY message")
        self.id = ID
        self.drone_indices = [ID + i for i in range(NUM_BOTS)]
        send_packet(self.socket, HIVE_READY_MESSAGE)

    def run(self):
        try:
            # Packet loop.
            while True:
                print("[HIVEMIND] Receiving packet")
                packet = receive_packet(self.socket)
                self.parse_packet(packet)

        except Exception as e:
            print(e)
            print("[HIVEMIND] Closing")
            self.socket.close()

    def parse_packet(self, packet):
        # Packet is a list of messages.
        for message in packet:
            if message["type"] == "Update":
                print("[HIVEMIND] Received UPDATE message")
                self.get_output(message)

            else:
                # TODO Other kinds of messages
                continue

    def get_output(self, message):
        print("[HIVEMIND] Sending INPUT message")

        inputs = [INPUT_MESSAGE for drone in self.drone_indices]

        send_packet(self.socket, inputs)

if __name__ == "__main__":
    hivemind = SocketHivemind(23234)
    hivemind.run()