import socket

from messages import send_packet, receive_packet, INPUT_MESSAGE

ID = 0
NUM_BOTS = 4

# Notice: multiplicity == 4, telling RLBot I want to control bots.
# Controlled IDs are [id, id + 1, id + 2, id + 3].
# There must be enough cars in the match config file to support this.
HIVE_READY_MESSAGE = {
    "type": "Ready",
    "name": "Hivemind",
    "team": 0,
    "id": ID,
    "multiplicity": NUM_BOTS
}


class SocketHivemind:

    def log(self, statement):
        if self.debug:
            print(f"[HIVEMIND] {statement}")

    def __init__(self, port, debug=False):
        self.debug = debug
        self.log("Loaded")

        # Create socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log("Attempting to connect")
        self.socket.connect(("localhost", port))
        self.log("Connected")

        self.id = ID
        self.drone_indices = [ID + i for i in range(NUM_BOTS)]
        self.log("Sending READY message")
        send_packet(self.socket, HIVE_READY_MESSAGE)

    def run(self):
        try:
            # Packet loop.
            while True:
                self.log("Receiving packet")
                packet = receive_packet(self.socket)
                self.parse_packet(packet)

        except Exception as e:
            print(e)
            self.log("Closing")
            self.socket.close()

    def parse_packet(self, packet):
        # Packet is a list of messages.
        for message in packet:
            if message["type"] == "Update":
                self.log("Received UPDATE message")
                output = self.get_output(message)

                self.log("Sending INPUT messages")
                send_packet(self.socket, output)

            else:
                # TODO Other kinds of messages
                continue

    def get_output(self, message):
        controls = [INPUT_MESSAGE for drone in self.drone_indices]  
        return controls

if __name__ == "__main__":
    hivemind = SocketHivemind(23234, debug=True)
    hivemind.run()