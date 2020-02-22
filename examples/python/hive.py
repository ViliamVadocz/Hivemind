from typing import Dict

from rlbot.utils.structures.bot_input_struct import PlayerInput
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.agents.hivemind.drone_agent import DroneAgent
from rlbot.agents.hivemind.python_hivemind import PythonHivemind

# Dummy agent to call request MyHivemind.
class Drone(DroneAgent):
    hive_path = __file__
    hive_key = 'ChangeThisKey'
    hive_name = 'Example Hivemind'
    

class MyHivemind(PythonHivemind):

    def initialize_hive(self, packet: GameTickPacket) -> None:
        self.logger.info('Initialised!')

        # Find out team by looking at packet.
        # drone_indices is a set, so you cannot just pick first element.
        index = next(iter(self.drone_indices))
        self.team = packet.game_cars[index].team

        self.last_time = 0.0
        self.timer = 0.0

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        # Calculate delta time and add to timer.
        game_time = packet.game_info.seconds_elapsed
        dt = game_time - self.last_time
        self.last_time = game_time
        self.timer += dt

        # Proclaim aliveness every three seconds.
        if self.timer > 3.0:
            self.logger.info(f'I am alive! Team: {self.team}')
            self.timer = 0.0

        return {index: PlayerInput(throttle=1.0) for index in self.drone_indices}