import os

from rlbot.parsing.custom_config import ConfigHeader, ConfigObject
from rlbot.agents.base_independent_agent import BaseIndependentAgent
from rlbot.botmanager.helper_process_request import HelperProcessRequest
from rlbot.utils.logging_utils import get_logger
from rlbot.utils.structures import game_interface

BOT_CONFIG_HIVE_HEADER = 'Bot Parameters'
HIVE_PATH_KEY = 'hivemind_path'
HIVE_NAME_KEY = 'hivemind_name'
HIVE_KEY_KEY = 'hivemind_key'

class DroneAgent(BaseIndependentAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.hivemind_path = None
    
    def run_independently(self, terminate_request_event):
        pass

    def get_helper_process_request(self) -> HelperProcessRequest:
        if self.is_hivemind_path_found():
            # Appends team to key so that each team has its own hivemind.
            key = f'{self.hivemind_key}{self.team}' 

            # Creates request for helper process.
            options = {
                'name': self.hivemind_name
            }
            return HelperProcessRequest(self.hivemind_path, key, options=options)

        return None

    def is_hivemind_path_found(self):
        return self.hivemind_path is not None and os.path.isfile(self.hivemind_path)

    def load_config(self, config_header: ConfigHeader):
        self.hivemind_path = config_header.getpath(HIVE_PATH_KEY)
        self.hivemind_name = config_header.get(HIVE_NAME_KEY)
        self.hivemind_key = config_header.get(HIVE_KEY_KEY)

    @staticmethod
    def create_agent_configurations(config: ConfigObject):
        params = config.get_header(BOT_CONFIG_HIVE_HEADER)
        params.add_value(HIVE_PATH_KEY, str, default=None,
                         description='Relative path to the hivemind file')
        params.add_value(HIVE_NAME_KEY, str, default=None,
                         description='Name of your hivemind that shows up in the console')
        params.add_value(HIVE_KEY_KEY, str, default=None,
                         description='Bots with the same key will be part of the same hivemind')
