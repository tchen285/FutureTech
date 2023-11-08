from tkinter import *
import os

class Page3:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")
        self.selected_descriptions = []  # To store the selected descriptions

        file_name = self.app.page1.file_name

        self.file_name_label = Label(self.frame, text=file_name, font=("Arial", 14), bg="white")
        self.file_name_label.pack(pady=20)

        back_button = Button(self.frame, text="Back to Page 2", font=("Arial", 18), bg="red", command=app.show_page2)
        back_button.pack(pady=20)

        continue_button = Button(self.frame, text="Continue", font=("Arial", 18), bg="red", command=app.show_page4)
        continue_button.pack(side="bottom", pady=20, anchor="center")

    def set_file_content(self, descriptions):
        # Create Checkbuttons for each description
        for description in descriptions:
            var = IntVar()  # Create an IntVar to track the state of each Checkbutton
            check_button = Checkbutton(self.frame, text=description, font = ("Arial", 18), variable=var)
            check_button.var = var  # Store the IntVar as an attribute of the Checkbutton
            check_button.pack(anchor=W)
            check_button.deselect()  # Deselect by default

    def get_selected_descriptions(self):
        # Get the selected descriptions based on the Checkbuttons' state
        self.selected_descriptions = [widget.cget("text") for widget in self.frame.winfo_children() if
                                      isinstance(widget, Checkbutton) and widget.var.get() == 1]
        return self.selected_descriptions

    def get_selected_coordinates(self):
        selected_coordinates = {}
        target_coordinates = []
        for widget in self.frame.winfo_children():
            if isinstance(widget, Checkbutton) and widget.var.get() == 1:
                description = widget.cget("text")
                print("Selected Description:", description)
                for coordinates in self.app.container_data:
                    if self.app.container_data[coordinates] == description:
                        print(coordinates)
                        target_coordinates.append(coordinates)
        return selected_coordinates, target_coordinates

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def update_file_name(self, file_path):
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        self.file_name_label.config(text=f"{file_name_no_extension}")
