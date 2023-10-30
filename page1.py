from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os

class Page1:
    def __init__(self, app):
        self.app = app

        self.frame = Frame(app.root, bg="white")
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        logo = PhotoImage(file="Logo.png")

        def resize_image(image, width, height):
            return image.subsample(5) # 5 represents the image is going to be 1/5 size of original
        self.small_logo = resize_image(logo, 572, 251)

        canvas_width = self.small_logo.width()
        canvas_height = self.small_logo.height()

        canvas = Canvas(self.frame, width=canvas_width, height=canvas_height, highlightthickness=0)
        canvas.create_image(0, 0, anchor='nw', image=self.small_logo)
        canvas.grid(row=0, column=0)

        label = Label(self.frame, text="Upload a manifest file", font=("Arial", 24), bg="white")
        label.grid(row=1, column=1, pady=20)

        self.file_entry = Entry(self.frame, font=("Arial", 18), justify='center', width=40)
        self.file_entry.grid(row=2, column=1, pady=20)

        browse_button = Button(self.frame, text="Browse", font=("Arial", 18), bg="blue", command=self.browse_file)
        browse_button.grid(row=2, column=2, pady=20)

        continue_button = Button(self.frame, text="Continue", font=("Arial", 18), bg="green", command=app.show_page2)
        continue_button.grid(row=4, column=1, pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file_path)

        # 读取文件内容并处理以去除不需要的字符
        with open(file_path, 'r') as file:
            lines = file.readlines()
            content = [line.strip() for line in lines if "NAN" not in line and "UNUSED" not in line]
            # 进一步处理文件内容以提取所需的部分并去掉花括号
            cleaned_content = [line.split("}, ")[1].replace("{", "").replace("}", "") for line in content]
            self.file_content = cleaned_content

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def show_file_content(self):
        # 在点击"Unloading and Loading"按钮后，将文件内容存储到Page2的file_content属性中
        self.app.page2.file_content = self.file_content
        self.app.page3.set_file_content(self.file_content)
        self.app.show_page3()