from typing import Dict

from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket

# Temporary workaround.
# Adding src/ directory to PYTHONPATH.
import sys
from pathlib import Path
path_to_src_python = Path(__file__).parent.parent.parent / 'src' / 'python'
sys.path.append(str(path_to_src_python))

from drone_agent import DroneAgent
from hivemind import Hivemind

# Dummy agent.
class Drone(DroneAgent):
    pass

class MyHivemind(Hivemind):

    def initialize_hive(self, packet: GameTickPacket) -> None:
        self.logger.info('Hello there!')
        self.test = True

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        if self.test:
            self.logger.info('I am alive!')
            self.test = False
        return {index: PlayerInput() for index in self.drone_indices}