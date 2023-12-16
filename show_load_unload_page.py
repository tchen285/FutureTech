from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring
import os
from tkinter import Canvas
from load_unload import FindLoadUnloadPath

class ShowLoadUnload:
    def __init__(self, app):
        self.app = app
        # self.matrix = matrix
        # self.container_data = container_data
        # self.container_weight = None  # Add this line to initialize container_weight

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

        # KG
        # self.start_matrix_tuple = tuple(map(tuple, matrix))
        # Set the size of each square in the UI graph as a class attribute
        self.square_size = 40

        # Create a Canvas for the 2D UI graph
        self.canvas = Canvas(self.frame, width=12 * self.square_size, height=8 * self.square_size, bg="white")
        self.canvas.grid(row=2, column=1, padx=20, pady=20)

        # Set up the 2D matrix (replace this with your actual matrix)
        self.matrix = [
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
            [None, 0, 0, 0, "Bird", 0, 0, 0, 0, 0, 0, None],
            [None, None, 0, "Cat", "Dog", 0, 0, "Lion", 0, 0, None, None]
        ]

        # Draw the initial 2D graph
        self.draw_2d_graph()

    def draw_2d_graph(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the 2D matrix on the canvas
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                value = self.matrix[row][col]
                color = "white" if value == 0 else "black" if value is None else "light blue"
                x1, y1 = col * self.square_size, row * self.square_size
                x2, y2 = x1 + self.square_size, y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if value:
                    # Display the name in the center of the square
                    text_x = (x1 + x2) / 2
                    text_y = (y1 + y2) / 2
                    self.canvas.create_text(text_x, text_y, text=value, font=("Arial", 10, "bold"))

    def update_2d_graph(self, matrix):
        # Update the internal matrix with the new values
        self.matrix = matrix

        # Redraw the 2D graph
        self.draw_2d_graph()

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

        self.label1.config(text=combined_text)

        print("可以看见我吗?")
        self.label1.update_idletasks()  # Update the label immediately
        self.start_button.config(state=NORMAL)  # Enable the button

    def reset(self):
        self.descriptions = []
        self.current_step = 0
        self.label1.config(text="")
        self.start_button.config(state=DISABLED)  # Disable the button initially
        self.new_task_button.grid_remove()

    def update_file_name(self, file_path):
        file_name = os.path.basename(file_path)
        file_name_no_extension = os.path.splitext(file_name)[0]
        self.file_name_label.config(text=f"{file_name_no_extension}")
