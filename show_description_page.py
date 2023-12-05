from tkinter import *

class ShowDescriptions:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.descriptions = []
        self.current_step = 0

        self.label1 = Label(self.frame, text="", font=("Arial", 20), bg="white", justify="center")
        self.label1.grid(row=0, column=0, padx=20, pady=20)

        self.start_button = Button(self.frame, text="Next Step", font=("Arial", 18), bg="red", command=self.next_step, state=DISABLED)
        self.start_button.grid(row=1, column=0, pady=20)

        self.new_task_button = Button(self.frame, text="Start a new task", font=("Arial", 18), bg="green", command=self.start_new_task)
        self.new_task_button.grid(row=2, column=0, pady=20)
        self.new_task_button.grid_remove()  # Initially hide the "Start a new task" button

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
            self.label1.config(text="Task done!\nDon't forget to send the updated manifest to the captain.")
            self.start_button.grid_remove()
            self.new_task_button.grid()

    def start_new_task(self):
        self.new_task_button.grid_remove()
        self.start_button.grid()
        self.app.show_page1()

    def update_label(self):
        self.label1.config(text=self.descriptions[self.current_step])
        self.start_button.config(state=NORMAL)  # Enable the button

    def reset(self):
        self.descriptions = []
        self.current_step = 0
        self.label1.config(text="")
        self.start_button.config(state=DISABLED)  # Disable the button initially
        self.new_task_button.grid_remove()
