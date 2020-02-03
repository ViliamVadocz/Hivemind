from typing import Dict

from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket

# I am hoping I can add this to rlbot
# or maybe make it a separate package like rlbot_hive.
from hivemind_source.drone_agent import DroneAgent
from hivemind_source.hivemind import Hivemind

# Dummy agent.
class Drone(DroneAgent):
    pass

class MyHivemind(Hivemind):

    def initialize_hive(self, packet: GameTickPacket) -> None:
        self.logger.info('Hello there!')
        self.test = True
        pass

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        if self.test:
            self.logger.info('I am alive!')
            self.test = False
        return {index: PlayerInput() for index in self.drone_indices}