import logging
import tkinter as tk

import hou  # type: ignore

from launcher.edit import *
from launcher.KeyHandler import KeymapReader
from launcher.keymap import *
from launcher.NetworkType import NetworkType

# IMPORTANT for proper VSCode intellisense to work
try:
    from KeyHandler import KeymapReader
    from NetworkType import NetworkType
except Exception as _:
    pass


def on_key_press(event):
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

        keymap_reader = KeymapReader()
        keymap = keymap_reader.key_map
        pprint.pp(keymap)
        root.destroy()
        return

    print(f"Key Pressed: {event.keysym}")

    try:
        s = KeymapReader()
        network_type = NetworkType.get_network_type(hou.ui.paneTabUnderCursor().pwd())
        # print(network_type.value)
        # print(s.key_map)
        action = s.ParseKey(network_type.value, str(event.keysym))
        action.Execute()
    except Exception as e:
        print(e)
        # logging.error("Unable to create. Perhaps check the name?")
    root.destroy()


def on_focus_out(_):
    print("No input detected")
    root.destroy()


def hook_window():
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
    root.bind("<KeyPress>", lambda event: on_key_press(event))
    root.bind("<FocusOut>", on_focus_out)
    root.mainloop()


hook_window()
