import tkinter as tk
import hou

from launcher.edit import *
from launcher.keymap import *


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
    except:
        print(f"{event.keysym} is not bound")
        root.destroy()
        return
        # keymap_append("sop", "m", "merge")

    global network_node, cursor_loc
    try:
        created_node = network_node.createNode(node)
        created_node.setPosition(cursor_loc)
    except:
        logging.error(f"Unable to create {node}. Perhaps check the name?")
    root.destroy()


def on_focus_out(_):
    print("No input detected")
    root.destroy()


def hook_window():
    global root
    # Create the main window
    root = tk.Tk()
    root.geometry("300x200")
    label = tk.Label(root,
                     text="Press any key...\nPress ` to add a binding\n Press Del to remove binding\nPress Tab to show bindings",
                     font=("Arial", 12))

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
