import logging
import tkinter as tk

from launcher.keymap import *


def window_add_keymap():
    # Create the main window
    subwindow = tk.Tk()
    subwindow.title("Enter new mapping")
    subwindow.attributes('-topmost', 'true')

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

    def sub_focus_out(event):
        logging.info("Exit subwindow due to focus loss")
        subwindow.destroy()

    def window_add_check_input(event):
        if event.keysym == "Return":
            context = entry1.get()
            key = entry2.get()
            node = entry3.get()
            try:
                keymap_append(context, key, node)
            except:
                logging.error("Failed to add keymap entry")
                subwindow.destroy()
                return 0
            print(f"{context}:{key} added as bind for {node}")
            subwindow.destroy()
        elif event.keysym == "Escape":

            logging.info("Exited without adding key")
            subwindow.destroy()

    subwindow.bind("<KeyPress>", window_add_check_input)
    subwindow.mainloop()


def window_del_keymap():
    window_delete = tk.Tk()
    window_delete.title("Enter mapping to delete: Context | Key")
    window_delete.attributes('-topmost', 'true')

    window_width = 400
    window_height = 50

    # Get the screen width and height
    screen_width = window_delete.winfo_screenwidth()
    screen_height = window_delete.winfo_screenheight()

    # Calculate the center position
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))

    # Set the window size and position it in the center of the screen
    window_delete.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    entry1 = tk.Entry(window_delete, width=25)
    entry2 = tk.Entry(window_delete, width=25)
    entry1.pack(side=tk.LEFT, padx=5, pady=5)
    entry2.pack(side=tk.LEFT, padx=5, pady=5)

    # Focus on the window
    entry1.focus_force()

    # Bind the key press even

    def window_del_check_input(event):
        if event.keysym == "Escape":
            try:
                window_delete.destroy()
            except:
                logging.error("Unable to kill window_delete for some reason")
            return
        elif event.keysym == "Return":
            context = entry1.get()
            key = entry2.get()
            keymap_remove(context, key)
            try:
                window_delete.destroy()
            except:
                logging.error("Unable to kill window_delete for some reason")
            return
        return

    window_delete.bind("<KeyPress>", window_del_check_input)
    window_delete.mainloop()
