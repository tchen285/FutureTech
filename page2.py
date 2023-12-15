from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
from balancing import FindBalancingPath
import os
from datetime import datetime


class Page2:
    def __init__(self, app):
        self.operator_name_label = None
        self.app = app
        self.frame = Frame(app.root, bg="white")
        self.file_content = []

        self.file_name_label = Label(self.frame, text="", font=("Arial", 20), bg="white", fg="red")
        self.file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        unload_button = Button(self.frame, text="Loading / Unloading", font=("Arial", 20), bg="white", command=self.show_file_content)
        unload_button.grid(row=2, column=3, pady=20)

        balancing_button = Button(self.frame, text="Balancing", font=("Arial", 20), bg="white", command=self.calculate_balance)
        balancing_button.grid(row=3, column=3, pady=20)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.grid(row=0, column=4, padx=10, pady=10)

        # Add the comment button
        comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        comment_button.grid(row=5, column=1, padx=10, pady=10)

        # Display operator name label
        self.operator_name_label = Label(self.frame, text="Hello Name!", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=4, padx=10, pady=10)

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
        #current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")

        if operator_name:
            #if current_operator != "":
            # self.write_to_log(current_operator, "signs out", "page2")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")

        self.app.page3.update_operator_name(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        self.app.page3.update_operator_name(name)

    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")

    def handle_comment(self):
        # Prompt the user to enter an event
        current_operator = self.operator_name_label.cget("text").replace("Operator: ", "") + ":"
        event_comment = askstring("Comment", "Enter the event:")
        if event_comment:
            event_comment = '"'+  event_comment+ '"'
            self.write_to_log(current_operator, event_comment)

    def calculate_balance(self):
        balancing_path_finder = FindBalancingPath(self.app.original_matrix, self.app.page1.file_name)
        balancing_path_finder.solve_balancing()
        self.app.balance_list = balancing_path_finder.description_list
        descriptions = balancing_path_finder.description_list
        steps = len(balancing_path_finder.description_list)
        time_cost = balancing_path_finder.total_cost
        self.app.show_balance_cost_page()
        self.app.balance_cost_page.update_labels(steps, time_cost)
        self.app.description_page.update_descriptions(descriptions)

