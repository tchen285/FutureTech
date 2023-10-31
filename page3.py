from tkinter import *
from tkinter import ttk

class Page3:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")
        self.selected_descriptions = []  # To store the selected descriptions

        back_button = Button(self.frame, text="Back to Page 2", font=("Arial", 18), bg="red", command=app.show_page2)
        back_button.pack(pady=20)

    def set_file_content(self, descriptions):
        # Create Checkbuttons for each description
        for description in descriptions:
            var = IntVar()  # Create an IntVar to track the state of each Checkbutton
            check_button = Checkbutton(self.frame, text=description, variable=var)
            check_button.var = var  # Store the IntVar as an attribute of the Checkbutton
            check_button.pack(anchor=W)
            check_button.deselect()  # Deselect by default

    def get_selected_descriptions(self):
        # Get the selected descriptions based on the Checkbuttons' state
        self.selected_descriptions = [widget.cget("text") for widget in self.frame.winfo_children() if widget.var.get() == 1]
        return self.selected_descriptions

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()
