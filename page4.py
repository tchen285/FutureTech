from tkinter import *
import os

class Page4:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.file_name_label = Label(self.frame, text=self.app.page1.file_name, font=("Arial", 14), bg="white")
        self.file_name_label.pack(pady=20)


    def show_selected_descriptions(self):
        # Create a label to display selected descriptions
        descriptions_label = Label(self.frame, text="Selected Container(s):", font=("Arial", 18))
        descriptions_label.pack()

        # Create a text box to display selected descriptions
        descriptions_text = Text(self.frame, font=("Arial", 16), width=40, height=10)
        descriptions_text.pack()

        # Get selected descriptions from Page3
        selected_descriptions = self.app.page3.get_selected_descriptions()

        # Insert selected descriptions into the text box
        for description in selected_descriptions:
            descriptions_text.insert("end", description + "\n")

    def show(self):
        self.frame.grid()
        self.show_selected_descriptions()
        _, target_containers = self.app.page3.get_selected_coordinates()
        print(target_containers)


    def hide(self):
        self.frame.grid_remove()

    def update_file_name(self, file_path):
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        self.file_name_label.config(text=f"{file_name_no_extension}")
