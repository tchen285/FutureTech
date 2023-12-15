from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
from tkinter.simpledialog import askfloat
import os

class ShowLoadUnload:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.descriptions = []
        self.current_step = 0

        self.label1 = Label(self.frame, text="Can you see me?", font=("Arial", 20), bg="white", justify="center")
        self.label1.grid(row=1, column=1, padx=20, pady=20)

        self.start_button = Button(self.frame, text="Next Step", font=("Arial", 18), bg="red", command=self.next_step, state=DISABLED)
        self.start_button.grid(row=3, column=1, pady=20)

        self.new_task_button = Button(self.frame, text="Start a new task", font=("Arial", 18), bg="green", command=self.start_new_task)
        self.new_task_button.grid(row=4, column=1, pady=20)
        self.new_task_button.grid_remove()  # Initially hide the "Start a new task" button

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
            self.enter_weight_button = Button(self.frame, text="Enter weight", font=("Arial", 18), bg="blue",
                                              command=self.enter_weight)
            self.enter_weight_button.grid(row=5, column=1, pady=20)

    def enter_weight(self):
        # Prompt the user to enter the weight
        weight = askfloat("Enter Weight", "Enter the weight of the loading container:")
        if weight is not None:
            # Do something with the entered weight (e.g., store it, print it)
            print("Entered weight:", weight)

    def enter_weight(self):
        # Prompt the user to enter the weight
        weight = askfloat("Enter Weight", "Enter the weight of the loading container:")
        if weight is not None:
            # Do something with the entered weight (e.g., store it, print it)
            print("Entered weight:", weight)

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


