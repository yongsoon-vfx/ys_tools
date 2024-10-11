import logging
import tkinter as tk
from dataclasses import dataclass
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


@dataclass
class NodeCache:
    main_node: hou.Node
    child_node: hou.Node


class NodeArranger:
    def __init__(self, root_node: hou.Node):
        self.root_node = root_node
        self.children_recursive = []

    def gatherChildren(self):
        self.getChildren(self.root_node)

    def getChildren(self, node: hou.Node):
        for node_child in node.outputs():
            self.children_recursive.append(node_child)
            if len(node_child.outputs()) > 0:
                self.getChildren(node_child)


def check_state(selected_nodes: tuple[hou.Node]) -> NodeEditorState:
    selected_nodes_length = len(selected_nodes)
    if selected_nodes_length == 0:
        return NodeEditorState.NO_NODE_SELECTED
    if len(selected_nodes[0].outputs()) == 0:
        return NodeEditorState.LEAF_NODE_SELECTED
    return NodeEditorState.MIDDLE_NODE_SELECTED


def on_key_press(event, state):
    print(state)
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
        created_node: hou.Node = network_node.createNode(node)
        created_node.setPosition(cursor_loc)
        # Check State
        if state == NodeEditorState.MIDDLE_NODE_SELECTED:
            selected_node: hou.Node = hou.selectedNodes()[-1]

            nodes_cache = NodeCache(
                main_node=selected_node,
                child_node=selected_node.outputs()[0],
            )
            NA = NodeArranger(nodes_cache.child_node)
            NA.gatherChildren()
            print(nodes_cache.child_node)
            print(nodes_cache.main_node)
            created_node.setPosition(nodes_cache.main_node.position())
            created_node.move([0, -1])
            created_node.setInput(0, nodes_cache.main_node, 0)
            nodes_cache.child_node.move([0, -1])
            nodes_cache.child_node.setInput(0, created_node, 0)
            for output in NA.children_recursive:
                output.move([0, -1])
        if state == NodeEditorState.LEAF_NODE_SELECTED:
            selected_node: hou.Node = hou.selectedNodes()[-1]
            nodes_cache = NodeCache(
                main_node=selected_node,
                child_node=None,
            )
            print(nodes_cache.main_node)
            created_node.setPosition(nodes_cache.main_node.position())
            created_node.move([0, -1])
            created_node.setInput(0, nodes_cache.main_node, 0)

    except Exception as e:
        print(e)
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
    root.bind("<KeyPress>", lambda event: on_key_press(event, editor_state))
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
