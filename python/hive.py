from typing import Dict

from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket

# I am hoping I can add this to rlbot
# or maybe make it a separate package like rlbot_hive.
from hivemind_source.hivemind import Hivemind

class MyHivemind(Hivemind):

    def initialize_hive(self):
        self.logger.info('SUCCESS')
        pass

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        if packet.game_info.seconds_elapsed < 10.0:
            self.logger.info('RUNNING!')
        return {index: PlayerInput() for index in self.drone_indices}