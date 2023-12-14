from tkinter import *


class ShowLoadUnloadCost:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        # Initialize labels
        self.label1 = Label(self.frame, text=f"The load / unload process has 2 steps.", font=("Arial", 20), bg="white")
        self.label1.grid(row=0, column=0, pady=10)

        self.label2 = Label(self.frame, text="Takes 12 minutes to complete.", font=("Arial", 20), bg="white")
        self.label2.grid(row=1, column=0, pady=10)

        self.start_button = Button(self.frame, text="Start", font=("Arial", 18), bg="red", command=self.app.show_description_page)
        self.start_button.grid(row=2, column=0, pady=20)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()


    # def update_labels(self, steps, time):
    #     self.label1.config(text=f'The balance process has {steps} steps.')
    #     self.label2.config(text=f'Takes {time} minutes to complete.')


