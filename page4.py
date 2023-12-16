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
        self.loading_containers = []
        self.final_sequence = []

        self.file_name_label = Label(self.frame, text=self.app.page1.file_name, font=("Arial", 14), bg="white", fg="red")
        self.file_name_label.pack(pady=20)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check In", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.pack(pady=20)

        continue_button = Button(self.frame, text="Continue", font=("Arial", 18), bg="light green",
                                 command=self.continue_clicked)
        continue_button.pack(side="bottom", pady=20)

        # Add the comment button
        comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        comment_button.pack(pady=20)

        self.operator_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.operator_name_label.pack(pady=20)

        self.unload_sequence_var = StringVar()
        self.unload_descriptions_var = StringVar()
        self.unload_time_cost_var = StringVar()  # Add this line

    def update_unload_result(self, descriptions, sequence, time_cost, loading_containers):
        # Method to update the unload result
        self.sequence = sequence
        self.descriptions = descriptions
        self.time_cost = time_cost
        self.loading_containers = loading_containers

        # Print the received data for debugging
        print("Debug: Page4 - Updated Sequence:", self.sequence)
        print("Debug: Page4 - Updated Descriptions:", self.descriptions)
        print("Debug: Page4 - Updated Loading_containers:", self.loading_containers)
        print(self.app.container_data[(1, 2)])  # call

        # Update the GUI elements with the received data
        self.unload_sequence_var.set(f"Unload Sequence: {self.sequence}")
        self.unload_descriptions_var.set(f"Descriptions: {self.descriptions}")
        self.unload_time_cost_var.set(f"Time Cost: {self.time_cost}")
        self.write_unload_log(self.sequence)
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

    def update_file_name(self, file_path, file_name):
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
            self.app.update_operator_name_all_pages(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        #self.app.load_unload_page.update_operator_name(name)

    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")

    def handle_comment(self):
        # Prompt the user to enter an event
        current_operator = self.operator_name_label.cget("text").replace("Operator: ", "") + " report:"
        event_comment = askstring("Comment", "Enter the event:")
        if event_comment:
            event_comment = '"'+  event_comment+ '"'
            self.write_to_log(current_operator, event_comment)

    def write_unload_log(self,text):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")

        # Log the information to the log file
        with open('log.txt', 'a') as log_file:
            log_file.write(f'{current_time} "{text}" is offloaded.\n')

    def continue_clicked(self):
        selected_coordinates, target_coordinates = self.app.page3.get_selected_coordinates()
        self.app.show_load_unload_cost_page()
        steps = len(self.descriptions)
        time_cost = self.time_cost
        self.final_sequence = self.merge_lists_alternatively()
        print("++++++++++++++++++++Final Sequence: ", self.final_sequence)
        self.app.load_unload_page.update_labels(steps, time_cost, self.final_sequence)

    def show_load_unload_cost_page(self):
        print("Debug: Load/Unload Cost Page - Sequence:", self.sequence)
        print("Debug: Load/Unload Cost Page - Descriptions:", self.descriptions)

    def get_sequence_and_descriptions(self):
        print("Page4 - Get Sequence and Descriptions - Sequence:", self.sequence)
        print("Page4 - Get Sequence and Descriptions - Descriptions:", self.descriptions)
        return self.sequence, self.descriptions

    def merge_lists_alternatively(self):
        # Extract the "name" list in loading_containers
        loading_container_names = [container["name"] for container in self.loading_containers]

        # Alternately merge sequence and loading_container_names
        result = [item for pair in zip(self.sequence, loading_container_names) for item in pair]

        # If a list is longer, add the remaining elements to the resulting list
        remaining_items = self.sequence[len(loading_container_names):] + loading_container_names[len(self.sequence):]
        result.extend(remaining_items)

        return result