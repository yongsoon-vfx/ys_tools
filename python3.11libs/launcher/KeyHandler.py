import logging
from pathlib import Path

import tomli_w as tomlw
import tomllib as toml

from launcher.Executor import Action

# Constants
KEYMAP_FILE_NAME = "KeyMap.toml"
KEYMAP_FILE_PATH = Path(__file__ + "/../" + KEYMAP_FILE_NAME)
INDENT_SPACING = 4


class KeymapReader:
    def __init__(self):
        # print(KEYMAP_FILE_PATH)
        if not KEYMAP_FILE_PATH.exists():
            print("Keymap Does not Exist")
        self.key_map = {}
        with open(KEYMAP_FILE_PATH, "rb") as f:
            self.key_map = toml.load(f)

    def ParseKey(self, network_context: str, key: str) -> Action:
        return Action(self.key_map[network_context][key])


class KeymapWriter:
    def __init__(self):
        print("end")


# c = KeymapReader()
# action = c.ParseKey("sop", "t")
# action.Execute()
# print(action.action)
