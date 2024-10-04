import logging
import tkinter as tk
from enum import Enum

import hou

from launcher.edit import *
from launcher.keymap import *


class NodeEditorState(Enum):
    NO_NODE_SELECTED = 0
    LEAF_NODE_SELECTED = 1
    MIDDLE_NODE_SELECTED = 2
    MULTIPLE_SELECTED = 3
    INVALID_NODE_STATE = 4


def check_state(selected_nodes: tuple[hou.Node]) -> NodeEditorState:
    if selected_nodes is None:
        return NodeEditorState.NO_NODE_SELECTED
    selected_nodes_length = len(selected_nodes)
    if selected_nodes_length == 0:
        return NodeEditorState.LEAF_NODE_SELECTED
    else:
        return NodeEditorState.MIDDLE_NODE_SELECTED
    return NodeEditorState.INVALID_NODE_STATE


def on_key_press(event):
    if event.char == "`":
        root.destroy()
        window_add_keymap()
        return
    elif event.keysym == "Escape":
        root.destroy()
        return
    elif event.keysym == "Delete":
        root.destroy()
        window_del_keymap()
        return
    elif event.keysym == "Tab":
        import pprint

        keymap = keymap_load()
        pprint.pp(keymap)
        root.destroy()
        return

    print(f"Key Pressed: {event.keysym}")
    try:
        node = keymap_lookup("sop", str(event.keysym))
    except Exception as _:
        print(f"{event.keysym} is not bound")
        root.destroy()
        return
        # keymap_append("sop", "m", "merge")

    global network_node, cursor_loc
    try:
        created_node = network_node.createNode(node)
        created_node.setPosition(cursor_loc)
    except Exception as _:
        logging.error(f"Unable to create {node}. Perhaps check the name?")
    root.destroy()


def on_focus_out(_):
    print("No input detected")
    root.destroy()


def hook_window():
    editor_state = check_state(hou.selectedNodes())
    global root
    # Create the main window
    root = tk.Tk()
    root.geometry("300x200")
    label = tk.Label(
        root,
        text="Press any key...\nPress ` to add a binding\n Press Del to remove binding\nPress Tab to show bindings",
        font=("Arial", 12),
    )

    label.pack(expand=True)
    root.overrideredirect(True)
    # Focus on the window
    root.focus_force()
    # Bind the key press event
    root.bind("<KeyPress>", on_key_press)
    root.bind("<FocusOut>", on_focus_out)
    root.mainloop()


def get_network_tab_location():
    network_tab = hou.ui.paneTabUnderCursor()
    node = network_tab.pwd()
    cursor_loc = network_tab.cursorPosition()
    logging.debug(f"Cursor Location:{cursor_loc}")
    logging.debug(f"Node Path:{node}")

    return cursor_loc, node


cursor_loc, network_node = get_network_tab_location()
hook_window()
