import logging
import tkinter as tk
from dataclasses import dataclass
from enum import Enum

import hou

from launcher.edit import *
from launcher.keymap import *

# Layout Constants
VERTICAL_SPACING = [0, -1]


class NodeEditorState(Enum):
    NO_ITEM_SELECTED = 0
    LEAF_NODE_SELECTED = 1
    MIDDLE_NODE_SELECTED = 2
    CONNECTOR_SELECTED = 3
    MULTIPLE_NODE_SELECTED = 4
    MULTIPLE_CONNECTIONS_SELECTED = 5
    INVALID_NODE_STATE = 6

    @classmethod
    def check_state() -> NodeEditorState:
        selected_nodes = hou.selectedNodes()
        selected_connections = hou.selectedConnections()

        if len(selected_nodes) == 0 and len(selected_connections) == 0:
            return NodeEditorState.NO_ITEM_SELECTED

        if len(selected_nodes) > 0:
            if len(selected_nodes[0].outputs()) == 0:
                return NodeEditorState.LEAF_NODE_SELECTED

            if len(selected_nodes[0].outputs()) >= 1:
                return NodeEditorState.MIDDLE_NODE_SELECTED

        if len(selected_connections) >= 1:
            return NodeEditorState.CONNECTOR_SELECTED


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


class NodeFactory:
    def __init__(
        self, node_type_name: str, network: hou.Node, state: NodeEditorState, **kwargs
    ):
        """
        A class used to handle creating a hou.Node and arranging it
        in the correct position in the tree

        Args:
            node_type_name (str): _description_
            network (hou.Node): _description_
            state (NodeEditorState): _description_
            cursor_location (hou.Vector2,optional): _description_
        """
        self.created_node: hou.Node = network.createNode(node_type_name)

        if state in [
            NodeEditorState.LEAF_NODE_SELECTED,
            NodeEditorState.MIDDLE_NODE_SELECTED,
        ]:
            self.selected_node: hou.Node = hou.selectedNodes()[-1]
        self.state = state
        self.cursor_location = kwargs.get("cursor_location", None)

        self.createNode()
        self.created_node.setGenericFlag(hou.nodeFlag.Display, True)
        self.created_node.setGenericFlag(hou.nodeFlag.Render, True)

    def createNode(self) -> int:
        match self.state:
            case NodeEditorState.NO_ITEM_SELECTED:
                node_location = self.cursor_location
                self.created_node.setPosition(node_location)
                return 0

            case NodeEditorState.LEAF_NODE_SELECTED:
                self.created_node.setPosition(self.selected_node.position())
                self.created_node.move(VERTICAL_SPACING)
                self.created_node.setInput(0, self.selected_node)
                return 0

            case NodeEditorState.MIDDLE_NODE_SELECTED:
                child_node: hou.Node = self.selected_node.outputs()[0]
                input_connection_idx = 0
                for i, node in enumerate(child_node.inputs()):
                    print(node)
                    if node == self.selected_node:
                        input_connection_idx = i
                print(f"input idx is {input_connection_idx}")
                NA = NodeArranger(child_node)
                NA.gatherChildren()
                self.created_node.setPosition(self.selected_node.position())
                self.created_node.move(VERTICAL_SPACING)
                self.created_node.setInput(0, self.selected_node)
                child_node.move(VERTICAL_SPACING)
                child_node.setInput(input_connection_idx, self.created_node)
                for node in NA.children_recursive:
                    node.move(VERTICAL_SPACING)
                return 0
            case _:
                raise "Invalid Node State"


def on_key_press(event, state):
    # print(state)
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
        created_node = NodeFactory(
            node, network_node, state, cursor_location=cursor_loc
        )
    except Exception as e:
        print(e)
        logging.error(f"Unable to create {node}. Perhaps check the name?")
    root.destroy()


def on_focus_out(_):
    print("No input detected")
    root.destroy()


def hook_window():
    editor_state = check_state()
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
