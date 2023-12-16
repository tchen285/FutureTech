from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
from tkinter.simpledialog import askfloat
import os
from datetime import datetime

import page1

class ShowLoadUnload:
    def __init__(self, app):
        self.app = app
        self.page1 = page1
        self.frame = Frame(app.root, bg="white")

        self.descriptions = []
        self.current_step = 0

        self.label1 = Label(self.frame, text="Can you see me?", font=("Arial", 20), bg="white", justify="center")
        self.label1.grid(row=1, column=1, padx=20, pady=20)

        self.start_button = Button(self.frame, text="Next Step", font=("Arial", 18), bg="red", command=self.next_step, state=DISABLED)
        self.start_button.grid(row=3, column=1, pady=20)

        self.new_task_button = Button(self.frame, text="Start a New Task", font=("Arial", 18), bg="green", command=self.start_new_task)
        self.new_task_button.grid(row=4, column=1, pady=20)
        self.new_task_button.grid_remove()  # Initially hide the "Start a new task" button

        self.set_operator_name_button = Button(self.frame, text="Check In", font=("Arial", 14), bg="orange",
                                               command=self.set_operator_name)
        self.set_operator_name_button.grid(row=0, column=4, padx=10, pady=10)

        self.operator_name_label = Label(self.frame, text="Enter Your Name Please", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=4, padx=10, pady=10)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def update_descriptions(self, descriptions):
        self.descriptions = descriptions
        self.current_step = 0
        self.update_label()
        print("Debug: ShowLoadUnload Frame is Shown")

    def next_step(self):
        if self.current_step < len(self.descriptions) - 1:
            self.current_step += 1
            self.update_label()
        else:
            self.label1.config(text="Task done!\n\nDon't forget to send the updated manifest to the captain.")
            self.start_button.grid_remove()
            self.new_task_button.grid()

    def start_new_task(self):
        self.new_task_button.grid_remove()
        self.start_button.grid()
        self.app.show_page1()

    def update_label(self):
        step_info = f"Step {self.current_step + 1}/{len(self.descriptions)}"
        description_text = self.descriptions[self.current_step]
        combined_text = f"{step_info}\n\n{description_text}"

        print("Debug: Current Step -", self.current_step)
        print("Debug: Description Text -", description_text)
        print("Debug: Combined Text in ShowLoadUnload -", combined_text)

        self.label1.config(text=combined_text)
        self.label1.update_idletasks()  # Update the label immediately
        self.start_button.config(state=NORMAL)  # Enable the button

        # Check if the current description contains the keyword
        if "Take the loading container" in description_text:
            # Display the "Enter weight" button
            self.enter_weight_button = Button(self.frame, text="Enter Weight", font=("Arial", 18), bg="light blue",
                                              command=self.enter_weight)
            self.enter_weight_button.grid(row=5, column=1, pady=20)

    def enter_weight(self):
        # Prompt the user to enter the weight
        weight = askfloat("Enter Weight", "Enter the Weight of the Loading Container:")
        if weight is not None:
            # Do something with the entered weight (e.g., store it, print it)
            print("Entered weight:", weight)

    # def enter_weight(self):
    #     # Prompt the user to enter the weight
    #     weight = askfloat("Enter Weight", "Enter the weight of the loading container:")
    #     if weight is not None:
    #         # Do something with the entered weight (e.g., store it, print it)
    #         print("Entered weight:", weight)

    def reset(self):
        self.descriptions = []
        self.current_step = 0
        self.label1.config(text="")
        self.start_button.config(state=DISABLED)  # Disable the button initially
        self.new_task_button.grid_remove()

    def update_file_name(self, file_path):
        print(f"$$$$$Updating File Name with Path: {file_path}")
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        print(f"$$$$$Updated File Name: {file_name_no_extension}")
        self.file_name_label.config(text=f"{file_name_no_extension}")


    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")

        if operator_name:
            #if current_operator != "":
                #self.write_to_log(current_operator, "signs out","page4")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")
            self.app.page1.update_operator_name(operator_name)
    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        #self.app.page1.update_operator_name(name)
    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")


