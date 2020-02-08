from typing import Dict

import queue
import time

from rlbot.botmanager.agent_metadata import AgentMetadata
from rlbot.botmanager.bot_helper_process import BotHelperProcess
from rlbot.messages.flat import MatchSettings
from rlbot.utils.game_state_util import GameState
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.structures.ball_prediction_struct import BallPrediction
from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket, FieldInfoPacket
from rlbot.utils.structures.game_interface import GameInterface

class Hivemind(BotHelperProcess):

    # Terminology:
    # hivemind - main process controlling the drones.
    # drone - a bot under the hivemind's control.

    def __init__(self, agent_metadata_queue, quit_event, options):
        super().__init__(agent_metadata_queue, quit_event, options)

        # Sets up the logger. The string is the name of your hivemind.
        # This is configured inside your config file under hivemind_name.
        self.logger = get_logger(options['name'])

        # The game interface is how you get access to things
        # like ball prediction, the game tick packet, or rendering.
        self.game_interface = GameInterface(self.logger)

        # drone_indices is a set of bot indices
        # which requested this hivemind with the same key.
        self.drone_indices = set()


    def try_receive_agent_metadata(self):
        """Adds all drones with the correct key to our set of running indices."""
        while not self.metadata_queue.empty():
            # Tries to get the next agent from the queue.
            single_agent_metadata: AgentMetadata = self.metadata_queue.get(timeout=0.1)
            # Adds the index to the drone_indices.
            self.drone_indices.add(single_agent_metadata.index)


    def start(self):
        """Starts the BotHelperProcess - Hivemind."""
        # Prints an activation message into the console.
        # This lets you know that the process is up and running.
        self.logger.info("Hello, world!")

        # Loads game interface.
        self.game_interface.load_interface()

        # Wait a moment for all agents to have a chance to start up and send metadata.
        # Increase the time if you're having issues with drones missing from the hivemind.
        self.logger.info("Snoozing for 3 seconds; give me a moment.")
        time.sleep(3)
        self.try_receive_agent_metadata()
        self.logger.info("Finished sleeping. Ready to go!")

        # Runs the game loop where the hivemind will spend the rest of its time.
        self.__game_loop()


    def __game_loop(self):
        """
        The bot hivemind will stay in this loop for the whole game. 
        This is where the initialize_hive and get_outputs functions are called.
        """

        # Creating ball prediction and field info objects to later update in wrapper methods.
        self._ball_prediction = BallPrediction()
        self._field_info = FieldInfoPacket()
        self.game_interface.update_field_info_packet(self._field_info)
        # Wrapper for renderer.
        self.renderer = self.game_interface.renderer

        # Create packet object.
        packet = GameTickPacket()
        self.game_interface.update_live_data_packet(packet)
        
        # Initialization step for your hivemind.
        self.initialize_hive(packet)

        while True:
            previous_packet_time = packet.game_info.seconds_elapsed

            # Updating the packet.
            self.game_interface.update_live_data_packet(packet)

            # Checking if packet is old. If yes, sleep and skip running the code.
            if previous_packet_time == packet.game_info.seconds_elapsed:
                time.sleep(0.001)
                continue
            
            # Get outputs from hivemind for each bot.
            # Outputs are expected to be a Dict[int, PlayerInput]
            outputs = self.get_outputs(packet)

            if len(outputs) < len(self.drone_indices):
                self.logger.error('Not enough outputs were given.')
            
            elif len(outputs) > len(self.drone_indices):
                self.logger.error('Too many outputs were given.')
                
            # Send the drone inputs to the drones.
            for index in outputs:
                if index not in self.drone_indices:
                    self.logger.error('Tried to send output to bot index not in drone_indices.')
                    continue
                output = outputs[index]
                self.game_interface.update_player_input(
                    output, index)

    # Override these methods:

    def initialize_hive(self, packet: GameTickPacket) -> None:
        """
        Override this method if you want to have an initialization step for your hivemind.
        """
        pass

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        """Where all the logic of your hivemind gets its input and returns its outputs for each drone.
        
        Use self.drone_indices to access the set of bot indices your hivemind controls.
        
        Arguments:
            packet {GameTickPacket} -- see https://github.com/RLBot/RLBot/wiki/Input-and-Output-Data-(current)
        
        Returns:
            Dict[int, PlayerInput] -- A dictionary with drone indices as keys and corresponding PlayerInputs as values.
        """
        return {index: PlayerInput() for index in self.drone_indices}

    # Wrapper methods to make them the same as if you were making a normal python bot:

    def get_ball_prediction_struct(self) -> BallPrediction:
        self.game_interface.update_ball_prediction(self._ball_prediction)
        return self._ball_prediction

    def get_field_info(self) -> FieldInfoPacket:
        # Field info does not need to be updated.
        return self._field_info

    def get_match_settings(self) -> MatchSettings:
        return self.game_interface.get_match_settings()

    def set_game_state(self, game_state: GameState) -> None:
        self.game_interface.set_game_state(game_state)

    # Not everything is supported yet, e.g. quick chats and match comms.
