from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
import os

class ShowDescriptions:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.descriptions = []
        self.current_step = 0

        self.file_name_label = Label(self.frame, text="file_name", font=("Arial", 20), bg="white", fg="red")
        self.file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.label1 = Label(self.frame, text="", font=("Arial", 20), bg="white", justify="center")
        self.label1.grid(row=1, column=1, padx=20, pady=20)

        self.start_button = Button(self.frame, text="Next Step", font=("Arial", 18), bg="red", command=self.next_step, state=DISABLED)
        self.start_button.grid(row=2, column=1, pady=20)

        self.new_task_button = Button(self.frame, text="Start a new task", font=("Arial", 18), bg="green", command=self.start_new_task)
        self.new_task_button.grid(row=3, column=1, pady=20)
        self.new_task_button.grid_remove()  # Initially hide the "Start a new task" button

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

    def update_descriptions(self, descriptions):
        self.descriptions = descriptions
        self.current_step = 0
        self.update_label()

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

        self.label1.config(text=combined_text)
        self.start_button.config(state=NORMAL)  # Enable the button

    def reset(self):
        self.descriptions = []
        self.current_step = 0
        self.label1.config(text="")
        self.start_button.config(state=DISABLED)  # Disable the button initially
        self.new_task_button.grid_remove()

    def update_file_name(self, file_path):
        print(f"$$$$$Updating file name with path: {file_path}")
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        print(f"$$$$$Updated file name: {file_name_no_extension}")
        self.file_name_label.config(text=f"{file_name_no_extension}")

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


