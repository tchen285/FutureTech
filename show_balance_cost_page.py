from tkinter import *
from datetime import datetime
from tkinter.simpledialog import askstring


class ShowBalanceCost:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        # Initialize labels
        self.label1 = Label(self.frame, text=f"The balance process has 2 steps.", font=("Arial", 20), bg="white")
        self.label1.grid(row=0, column=0, pady=10)

        self.label2 = Label(self.frame, text="Takes 12 minutes to complete.", font=("Arial", 20), bg="white")
        self.label2.grid(row=1, column=0, pady=10)

        self.label3 = Label(self.frame, text="", font=("Arial", 20), bg="white")
        self.label3.grid(row=2, column=0, pady=10)

        self.label4 = Label(self.frame, text="", font=("Arial", 20), bg="white")
        self.label4.grid(row=3, column=0, pady=10)

        self.start_button = Button(self.frame, text="Start", font=("Arial", 18), bg="red", command=self.app.show_description_page)
        self.start_button.grid(row=4, column=0, pady=20)

        # Add a button to set operator name
        self.set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        self.set_operator_name_button.grid(row=0, column=4, padx=10, pady=10)

        # Add the comment button
        self.comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        self.comment_button.grid(row=5, column=1, padx=10, pady=10)

        # Display operator name label
        self.operator_name_label = Label(self.frame, text="Hello Name!", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=4, padx=10, pady=10)

    def show(self):
        self.frame.grid()


    def hide(self):
        self.frame.grid_remove()

    def update_labels(self, steps, time, sift):
        if sift:
            self.label1.config(text="This ship cannot be balanced")
            self.label2.config(text="Need to perform a SIFT process")
            self.label3.config(text=f'The SIFT process has {steps} steps.')
            self.label4.config(text=f'Takes {time} minutes to complete.')
        else:
            self.label1.config(text=f'The balance process has {steps} steps.')
            self.label2.config(text=f'Takes {time} minutes to complete.')
            self.write_balancing_log("Balancing complete")

    def write_balancing_log(self, text):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")

        # Log the information to the log file
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{current_time}  {text}.\n")

    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")
        # current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")

        if operator_name:
            # if current_operator != "":
            # self.write_to_log(current_operator, "signs out", "page2")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")

        self.app.update_operator_name_all_pages(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        # self.app.page3.update_operator_name(name)

    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")

    def handle_comment(self):
        # Prompt the user to enter an event
        current_operator = self.operator_name_label.cget("text").replace("Operator: ", "") + " report:"
        event_comment = askstring("Comment", "Enter the event:")
        if event_comment:
            event_comment = '"' + event_comment + '"'
            self.write_to_log(current_operator, event_comment)
