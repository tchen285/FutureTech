from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
from balancing import FindBalancingPath
import os

class Page2:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.file_content = []

        self.file_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white", fg="red")
        self.file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        unload_button = Button(self.frame, text="Loading / Unloading", font=("Arial", 18), bg="white", command=self.show_file_content)
        unload_button.grid(row=2, column=0, pady=20)

        balancing_button = Button(self.frame, text="Balancing", font=("Arial", 18), bg="white", command=self.calculate_balance)
        balancing_button.grid(row=3, column=0, pady=20)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.grid(row=0, column=1, padx=10, pady=10)

        # Display operator name label
        self.operator_name_label = Label(self.frame, text="Hello Name!", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=1, padx=10, pady=10)

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

    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")
        if operator_name:
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")

        self.app.page3.update_operator_name(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        self.app.page3.update_operator_name(name)

    def calculate_balance(self):
        balancing_path_finder = FindBalancingPath(self.app.original_matrix)
        balancing_path_finder.solve_balancing()
        self.app.balance_list = balancing_path_finder.description_list
        descriptions = balancing_path_finder.description_list
        steps = len(balancing_path_finder.description_list)
        time_cost = balancing_path_finder.total_cost
        self.app.show_balance_cost_page()
        self.app.balance_cost_page.update_labels(steps, time_cost)
        self.app.description_page.update_descriptions(descriptions)

