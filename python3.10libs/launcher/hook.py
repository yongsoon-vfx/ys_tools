import tkinter as tk
from pathlib import Path


def on_key_press(event):
    if event.char == "`":
        root.destroy()
        window_add_keymap()
        return
    print(f"Key pressed: {event.keysym}")
    try:
        keymap_lookup("sop", str(event.keysym))
    except:
        print(f"{event.keysym} is not bound")
        # keymap_append("sop", "m", "merge")
    root.destroy()


def on_focus_out(_):
    print("No input detected")
    root.destroy()


def keymap_lookup(context: str, key: str):
    keymap = keymap_load()
    print(keymap[context][key])


def keymap_load():
    import json

    keymap_json = Path(__file__ + "/../keymap.json")
    keymap = {}
    with open(keymap_json) as f:
        keymap = json.load(f)
    return keymap


def keymap_append(context: str, key: str, node: str):
    import json
    keymap = keymap_load()
    key_pair = {key: node}
    keymap[context][key] = node

    keymap_json = Path(__file__ + "/../keymap.json")
    with open(keymap_json, "w") as file:
        json.dump(keymap, file, indent=4)


def hook_window():
    global root
    # Create the main window
    root = tk.Tk()
    root.geometry("300x200")
    label = tk.Label(root, text="Press any key...", font=("Arial", 16))
    label.pack(expand=True)
    root.overrideredirect(True)
    # Focus on the window
    root.focus_force()
    # Bind the key press event
    root.bind("<KeyPress>", on_key_press)
    root.bind("<FocusOut>", on_focus_out)
    root.mainloop()
    exit()


def window_add_keymap():
    # Create the main window
    subwindow = tk.Tk()
    subwindow.title("Enter new mapping")

    window_width = 400
    window_height = 50

    # Get the screen width and height
    screen_width = subwindow.winfo_screenwidth()
    screen_height = subwindow.winfo_screenheight()

    # Calculate the center position
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))

    # Set the window size and position it in the center of the screen
    subwindow.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Create three text inputs side by side
    entry1 = tk.Entry(subwindow, width=20)
    entry2 = tk.Entry(subwindow, width=20)
    entry3 = tk.Entry(subwindow, width=20)
    entry1.focus_force()

    # Pack the entries side by side
    entry1.pack(side=tk.LEFT, padx=5, pady=5)
    entry2.pack(side=tk.LEFT, padx=5, pady=5)
    entry3.pack(side=tk.LEFT, padx=5, pady=5)

    # Start the tkinter event loop

    def check_enter(event):
        if event.keysym == "Return":
            context = entry1.get()
            key = entry2.get()
            node = entry3.get()

            keymap_append(context, key, node)
            print(f"{context}:{key} added as bind for {node}")
            subwindow.destroy()
        elif event.keysym == "Escape":
            print("Exited without adding key")
            subwindow.destroy()

    subwindow.bind("<KeyPress>", check_enter)

    subwindow.mainloop()


hook_window()
