"""Example messages and message management."""
# Inspiration from TheBeard's code: https://github.com/oxrock/python-rlbot-socket-example
# Socket RLBot wiki: https://github.com/samuelpmish/RLBot/wiki/JSON-Message-Specification

import json
import socket
import struct

ENCODING = "ascii"

### Functions for handling messages ###

def create_header(encoded_message):
    length = len(encoded_message)
    header = struct.pack("H", length)
    return header


def send_packet(socket, *args):
    # If there is only one argument and it is a list or tuple, use it as packet.
    if len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], tuple)):
        messages = args[0]
    # Otherwise treat each argument as message and send them as packet.
    else:
        messages = args
    # Encode to byte string.
    encoded_message = json.dumps(messages).encode(ENCODING)
    byte_message = bytes(encoded_message)
    # Create header (contains length of message)
    header = create_header(encoded_message)
    # Prepend header to message.
    byte_message = header + byte_message
    # Send message.
    socket.sendall(byte_message)

# XXX I have not tested this.
def receive_packet_pessimistic(socket):
    received = socket.recv(1024)
    # Get header.
    header = received[:2]
    encoded_packet = received[2:]
    # Unpack returns tuple and we want the value inside.
    length = struct.unpack("H", header)[0]
    # Receive rest of message.
    while len(encoded_packet) < length:
        what_is_left = length - len(encoded_packet)
        encoded_packet += socket.recv(min(what_is_left, 1024))
    # Convert from JSON.
    return json.loads(encoded_packet, encoding=ENCODING)


def receive_packet(socket):
    # Get header.
    received_header = socket.recv(2)
    # Unpack returns tuple and we want the value inside.
    length = struct.unpack("H", received_header)[0]
    # Receive rest of message.
    encoded_packet = socket.recv(length)
    # Convert from JSON.
    return json.loads(encoded_packet, encoding=ENCODING)

### From RLBot ###

INIT_MESSAGE = {
    "type": "Initialize",
    "map": "Mannfield",
    "mode": "soccer",
    "match_length": "5 minutes",
    "max_score": "unlimited",
    "overtime": "unlimited",
    "series": "unlimited",
    "speed": "default",
    "max_ball_speed": "default",
    "ball_shape": "default",
    "ball_weight": "default",
    "ball_size": "default",
    "ball_bounciness": "default",
    "boost": "default",
    "boost_strength": "default",
    "gravity": "default",
    "demolition": "default",
    "respawn": "3 seconds",

    "ball": {
            "shape": 0,
            "radius": 92.15,
            "height": -1.0
    },

    "cars": [{
        "name": "Botimus",
        "team": 0,
        "is_bot": True,
        "body_type": 0,
        "hitbox_offset": [0.2, 1.3, 0.2],
        "hitbox_dimensions": [65.0, 23.0, 120.0]
    }, {
        "name": "ReliefBot",
        "team": 0,
        "is_bot": True,
        "body_type": 0,
        "hitbox_offset": [0.2, 1.3, 0.2],
        "hitbox_dimensions": [65.0, 23.0, 120.0]
    }, {
        "name": "SDC",
        "team": 0,
        "is_bot": True,
        "body_type": 0,
        "hitbox_offset": [0.2, 1.3, 0.2],
        "hitbox_dimensions": [65.0, 23.0, 120.0]
    }
    ],

    "pads": [{
        "type": 0,
        "position": [1024.0, -512.0, 0.0]
    }, {
        "type": 0,
        "position": [1024.0, -512.0, 0.0]
    }, {
        "type": 0,
        "position": [1024.0, -512.0, 0.0]
    }
    ],

    "goals": [{
        "team": 0,
        "position": [0.0, -5120.0, 0.0],
        "direction": [0.0, 1.0, 0.0],
        "width": 600.0,
        "height": 500.0
    }, {
        "team": 1,
        "position": [0.0, 5120.0, 0.0],
        "direction": [0.0, -1.0, 0.0],
        "width": 600.0,
        "height": 500.0
    }
    ]
}


UPDATE_MESSAGE = {
    "type": "Update",
    "frame": 193,
    "time_left": 91,
    "state": "Kickoff",
    "score": [2, 3],
    "ball": {
            "position": [1.0, 2.0, 3.0],
            "velocity": [1.0, 2.0, 3.0],
            "euler_angles": [1.0, 2.0, 3.0],
            "angular_velocity": [1.0, 2.0, 3.0]
    },
    "cars": [{
        "position": [1.0, 2.0, 3.0],
        "velocity": [1.0, 2.0, 3.0],
        "euler_angles": [1.0, 2.0, 3.0],
        "angular_velocity": [1.0, 2.0, 3.0],
        "boost": 25,
        "state": "OnGround"
    }, {
        "position": [1.0, 2.0, 3.0],
        "velocity": [1.0, 2.0, 3.0],
        "euler_angles": [1.0, 2.0, 3.0],
        "angular_velocity": [1.0, 2.0, 3.0],
        "boost": 25,
        "state": "OnGround"
    }, {
        "position": [1.0, 2.0, 3.0],
        "velocity": [1.0, 2.0, 3.0],
        "euler_angles": [1.0, 2.0, 3.0],
        "angular_velocity": [1.0, 2.0, 3.0],
        "boost": 25,
        "state": "OnGround"
    }],
    "boost_pads": [0, 1, 0],
    "goals": [0, 0]
}


CUSTOM_MESSAGE = {
    "type": "Custom",
    "contents": "I've got it! Hitting ball on frame 281",
    "id": 0
}


TERMINATE_MESSAGE = {
    "type": "Terminate"
}

### To RLBot ###

READY_MESSAGE = {
    "type": "Ready",
    "name": "Botimus",
    "id": 0,
    "team": 0,
    "multiplicity": 1,  # >1 for hivemind
    "loadout": {
        "primary": [127, 255, 0],
        "secondary": [0, 255, 0],
        "car_id": 23,
        "car_paint_id": 12,
        "decal_id": 0,
        "decal_paint_id": 0,
        "wheels_id": 1565,
        "wheels_paint_id": 12,
        "boost_id": 35,
        "boost_paint_id": 7,
        "antenna_id": 0,
        "antenna_paint_id": 0,
        "hat_id": 0,
        "hat_paint_id": 0,
        "engine_audio_id": 0,
        "custom_finish_id": 1681,
        "paint_finish_id": 1681,
        "trails_id": 3220,
        "trails_paint_id": 2,
        "goal_explosion_id": 3018,
        "goal_explosion_paint_id": 0
    }
}

INPUT_MESSAGE = {
    "type": "PlayerInput",
    "steer": 1.0,
    "throttle": 1.0,
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "jump": 0,
    "boost": 0,
    "use_item": 0,
    "handbrake": 0
}

CAR_STATE_MESSAGE = {
    "type": "SetCarState",
    "id": 1,
    "position": [1.0, 2.0, 3.0],
    "velocity": [1.0, 2.0, 3.0],
    "euler_angles": [1.0, 2.0, 3.0],
    "angular_velocity": [1.0, 2.0, 3.0],
    "boost": 25
}

BALL_STATE_MESSAGE = {
    "type": "SetBallState",
    "position": [1.0, 2.0, 3.0],
    "velocity": [1.0, 2.0, 3.0],
    "euler_angles": [1.0, 2.0, 3.0],
    "angular_velocity": [1.0, 2.0, 3.0]
}
