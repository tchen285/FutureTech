from tkinter import *
from tkinter import filedialog
import os

class Page2:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.file_content = []

        self.file_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white", fg="red")
        self.file_name_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        unload_button = Button(self.frame, text="Unloading", font=("Arial", 18), bg="white", command=self.show_file_content)
        unload_button.grid(row=0, column=0, pady=20)

        load_button = Button(self.frame, text="Loading", font=("Arial", 18), bg="white")
        unload_button.grid(row=1, column=0, pady=20)

        balancing_button = Button(self.frame, text="Balancing", font=("Arial", 18), bg="white")
        balancing_button.grid(row=2, column=0, pady=20)

        back_button = Button(self.frame, text="Back", font=("Arial", 18), bg="red", command=app.show_page1)
        back_button.grid(row=3, column=0, pady=20)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def show_file_content(self):
        # Get the keys (descriptions) from container_data and filter out "NAN" and "UNUSED"
        descriptions = [description for description in self.app.container_data.values() if
                        description not in ["NAN", "UNUSED"]]
        self.app.page3.set_file_content(descriptions)
        self.app.show_page3()

    def update_file_name(self, file_path):
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        self.file_name_label.config(text=f"{file_name_no_extension}")


