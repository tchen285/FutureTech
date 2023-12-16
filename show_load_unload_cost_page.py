from tkinter import *
from datetime import datetime
from tkinter.simpledialog import askstring
import os
class ShowLoadUnloadCost:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        # Initialize labels
        self.label1 = Label(self.frame, text=f"Load / Unload Process has 2 Steps.", font=("Arial", 20), bg="white")
        self.label1.grid(row=0, column=0, pady=10)

        self.label2 = Label(self.frame, text="Takes 12 Minutes to Complete.", font=("Arial", 20), bg="white")
        self.label2.grid(row=1, column=0, pady=10)

        self.label3 = Label(self.frame, text="Takes 12 Minutes to Complete.", font=("Arial", 20), bg="white")
        self.label3.grid(row=2, column=0, pady=10)

        self.start_button = Button(self.frame, text="Start", font=("Arial", 18), bg="red", command=self.app.show_load_unload_page)
        self.start_button.grid(row=3, column=0, pady=20)

        self.set_operator_name_button = Button(self.frame, text="Check In", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        self.set_operator_name_button.grid(row=0, column=4, padx=10, pady=10)

        self.operator_name_label = Label(self.frame, text="Enter Your Name Please", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=4, padx=10, pady=10)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()


    def update_labels(self, steps, time, final_sequence):
        self.label1.config(text=f'The Balance Process has {steps} Steps')
        self.label2.config(text=f'Takes {time} Minutes to Complete')
        sequence = ' -> '.join(final_sequence)
        self.label3.config(text=f'The Sequence of Loading and Unloading: \n\n{sequence}')



    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")
        #current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")

        if operator_name:
            #if current_operator != "":
                #self.write_to_log(current_operator, "signs out","page4")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")
            self.app.show_load_unload_page.update_operator_name(operator_name)
    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        #self.app.show_load_unload_page.update_operator_name(name)

    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")
