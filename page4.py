from tkinter import *
from tkinter.simpledialog import askstring  # Import askstring for input dialog
import os
from datetime import datetime
from show_load_unload_cost_page import ShowLoadUnloadCost  # Import the relevant class



class Page4:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")
        self.sequence = []  # Initialize sequence attribute
        self.descriptions = []  # Initialize descriptions attribute

        self.file_name_label = Label(self.frame, text=self.app.page1.file_name, font=("Arial", 14), bg="white", fg="red")
        self.file_name_label.pack(pady=20)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.pack(pady=20)


        continue_button = Button(self.frame, text="Continue", font=("Arial", 18), bg="white",
                                 command=self.continue_clicked
        continue_button.pack(side="bottom", pady=20)

        # Add the comment button
        comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        comment_button.pack(pady=20)

        self.operator_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.operator_name_label.pack(pady=20)

        self.unload_sequence_var = StringVar()
        self.unload_descriptions_var = StringVar()

        # Create labels to display sequence and descriptions
        self.sequence_label = Label(self.frame, textvariable=self.unload_sequence_var, font=("Arial", 14), bg="white")
        self.sequence_label.pack(pady=20)

        self.descriptions_label = Label(self.frame, textvariable=self.unload_descriptions_var, font=("Arial", 14),
                                        bg="white")
        self.descriptions_label.pack(pady=20)

    def update_unload_result(self, descriptions, sequence):
        # Method to update the unload result
        self.sequence = sequence
        self.descriptions = descriptions

        # Print the received data for debugging
        print("Debug: Page4 - Updated Sequence:", self.sequence)
        print("Debug: Page4 - Updated Descriptions:", self.descriptions)

        # Update the GUI elements with the received data
        self.unload_sequence_var.set(f"Unload Sequence: {self.sequence}")
        self.unload_descriptions_var.set(f"Descriptions: {self.descriptions}")

    def get_selected_coordinates(self):
        # Your implementation for get_selected_coordinates in Page4
        pass



    def show_selected_descriptions(self):
        # Create a label to display selected descriptions
        descriptions_label = Label(self.frame, text="Selected Container(s):", font=("Arial", 18))
        descriptions_label.pack()

        # Create a text box to display selected descriptions
        descriptions_text = Text(self.frame, font=("Arial", 16), width=40, height=10)
        descriptions_text.pack()

        # Get selected descriptions from Page3
        selected_descriptions = self.app.page3.get_selected_descriptions()

        # Insert selected descriptions into the text box
        for description in selected_descriptions:
            descriptions_text.insert("end", description + "\n")

    def show(self):
        self.frame.grid()
        self.show_selected_descriptions()
        # self.app.page3.get_selected_coordinates()  # Remove this line
        print("********", self.sequence)
        print("********", self.descriptions)


    def hide(self):
        self.frame.grid_remove()

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
                #self.write_to_log(current_operator, "signs out","page4")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")
            self.app.page1.update_operator_name(operator_name)
    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")

    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")

    def handle_comment(self):
        # Prompt the user to enter an event
        current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")+ ":"
        event_comment = askstring("Comment", "Enter the event:")
        if event_comment:
            event_comment = '"'+  event_comment+ '"'
            self.write_to_log(current_operator, event_comment)

    def continue_clicked(self):
        selected_coordinates, target_coordinates = self.app.page3.get_selected_coordinates()
        self.show_load_unload_cost_page()

    def show_load_unload_cost_page(self):
        # Update the labels with the received data
        self.sequence_label.config(text=f"Unload Sequence: {self.sequence}")
        self.descriptions_label.config(text=f"Descriptions: {self.descriptions}")

        # Print for debugging
        print("Debug: Load/Unload Cost Page - Sequence:", self.sequence)
        print("Debug: Load/Unload Cost Page - Descriptions:", self.descriptions)

    def get_sequence_and_descriptions(self):
        print("Page4 - Get Sequence and Descriptions - Sequence:", self.sequence)
        print("Page4 - Get Sequence and Descriptions - Descriptions:", self.descriptions)
        return self.sequence, self.descriptions