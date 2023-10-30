from tkinter import *
from tkinter import filedialog

class Page2:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        self.file_content = []

        unload_button = Button(self.frame, text="Unloading and Loading", font=("Arial", 18), bg="white", command=self.show_file_content)
        unload_button.grid(row=0, column=0, pady=20)

        balancing_button = Button(self.frame, text="Balancing", font=("Arial", 18), bg="white")
        balancing_button.grid(row=1, column=0, pady=20)

        back_button = Button(self.frame, text="Back", font=("Arial", 18), bg="red", command=app.show_page1)
        back_button.grid(row=2, column=0, pady=20)

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def show_file_content(self):
        # 在点击"Unloading and Loading"按钮后，显示文件内容
        self.app.page3.set_file_content(self.app.page1.file_content)
        self.app.show_page3()
