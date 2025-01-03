# import hou
from enum import Enum
from pathlib import Path

from launcher.Actions import CreateNode


class ActionType(Enum):
    CREATE_NODE = "createnode"


class Action:
    def __init__(self, parsed_dict):
        self.__dict__.update(parsed_dict)

        if self.action is None:
            raise Exception("Error in Action: action attr is empty")

        self.action_type = ActionType(self.action)

        print(self.__dict__)

    def Execute(self) -> int:
        match self.action_type:
            case ActionType.CREATE_NODE:
                node_to_create = self.param
                network_state = CreateNode.NodeEditorState.check_state()
                cursor_loc, network_loc = (
                    CreateNode.NodeEditorState.get_network_tab_location()
                )
                CreateNode.NodeFactory(
                    node_to_create,
                    network_loc,
                    network_state,
                    cursor_location=cursor_loc,
                )
