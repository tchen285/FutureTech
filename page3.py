from tkinter import *
from tkinter.simpledialog import askstring  # Import askstring for input dialog
import os
from datetime import datetime
from load_unload import FindLoadUnloadPath
from show_load_unload_page import ShowLoadUnload
from os.path import join, expanduser

class Page3:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")
        self.selected_descriptions = []
        self.loading_containers = []
        self.descriptions = []
        self.sequence = []
        self.time_cost = 0
        self.file_path = ""
        self.file_name = ""

        file_name = self.app.page1.file_name
        self.show_load_unload_page = ShowLoadUnload(self.app)

        self.file_name_label = Label(self.frame, text=file_name, font=("Arial", 14), bg="white", fg="red")
        self.file_name_label.pack(pady=20)

        self.the_label = Label(self.frame, text="Select the Containers You Want to Unload", font=("Arial", 24), bg="white")
        self.the_label.pack(pady=20)

        continue_button = Button(self.frame, text="Continue", font=("Arial", 18), bg="light green", command=self.continue_clicked)
        continue_button.pack(side="bottom", pady=(10, 50))

        continue_with_loading_button = Button(self.frame, text="Adding Loading Containers", font=("Arial", 18), bg="yellow", command=self.add_loading_containers)
        continue_with_loading_button.pack(side="bottom", pady=10)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.pack(pady=20)

        # Add the comment button
        comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        comment_button.pack(pady=20)

        self.operator_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.operator_name_label.pack(pady=20)

    def continue_clicked(self):
        selected_coordinates, target_coordinates = self.get_selected_coordinates()
        self.app.page4.update_unload_result(self.descriptions, self.sequence, self.time_cost, self.loading_containers)
        self.app.show_load_unload_page.update_descriptions(self.descriptions)
        self.app.show_page4()

    def set_file_content(self, descriptions):
        # Create Checkbuttons for each description
        for description in descriptions:
            var = IntVar()  # Create an IntVar to track the state of each Checkbutton
            check_button = Checkbutton(self.frame, text=description, font = ("Arial", 18), variable=var)
            check_button.var = var  # Store the IntVar as an attribute of the Checkbutton
            check_button.pack(anchor=W)
            check_button.deselect()  # Deselect by default

    def get_selected_descriptions(self):
        # Get the selected descriptions based on the Checkbuttons' state
        self.selected_descriptions = [widget.cget("text") for widget in self.frame.winfo_children() if
                                      isinstance(widget, Checkbutton) and widget.var.get() == 1]
        return self.selected_descriptions

    def get_selected_coordinates(self):
        selected_coordinates = {}
        target_coordinates = []
        for widget in self.frame.winfo_children():
            if isinstance(widget, Checkbutton) and widget.var.get() == 1:
                description = widget.cget("text")
                for coordinates in self.app.container_data:
                    if self.app.container_data[coordinates] == description:
                        print(coordinates)
                        target_coordinates.append(coordinates)

        # testing start
        unload_finder = FindLoadUnloadPath(self.app.original_matrix, self.app.container_data, self.app.container_weight, self.file_name)
        # load_unload_finder.unload_set = target_coordinates
        for target_coordinate in target_coordinates:
            unload_finder.unload_set.add((8 - target_coordinate[0], target_coordinate[1] - 1))

        for loading_container in self.loading_containers:
            if isinstance(loading_container, dict):
                weight = loading_container["id"]
                unload_finder.load_list.append(weight)
                print(weight)

        self.sequence, self.descriptions, self.time_cost = unload_finder.solve_load_unload()

        return selected_coordinates, target_coordinates

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def update_file_name(self, file_path, file_name):
        self.file_name = file_name
        self.file_path = file_path

    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")
        #current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")

        if operator_name:
            #if current_operator != "":
                #self.write_to_log(current_operator, "signs out", "page3")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")

        self.app.update_operator_name_all_pages(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        #self.app.page4.update_operator_name(name)

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

    def add_loading_containers(self):
        container_name = askstring("Add Loading Containers", "Enter the container name:")

        # self.file_name = self.app.page1.file_name
        # print("dsa;sldkfj;alskdjgh;alksdjf", self.file_name)
        #
        # desktop_path = join(expanduser("~"), "Desktop")
        # filename = self.file_name
        # file_path = join(desktop_path, filename)

        if container_name:
            loading_container_id = 99999
            loading_container_name = f"{container_name} (loading)"
            var = IntVar()
            check_button = Checkbutton(self.frame, text=loading_container_name, font=("Arial", 18), variable=var)
            check_button.var = var
            check_button.pack(anchor=W)
            check_button.deselect()

            # Store the loading container information in the list
            loading_container_info = {
                "id": loading_container_id,
                "name": container_name,
                "display_name": loading_container_name
            }
            self.loading_containers.append(loading_container_info)

            self.write_load_log(loading_container_name)
            # self.container_weight[loading_container_name] = loading_container_id

    def write_load_log(self, loading_container_name):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")

        # Log the information to the log file
        with open('log.txt', 'a') as log_file:
            log_file.write(f'{current_time} "{loading_container_name}" is loaded.\n')