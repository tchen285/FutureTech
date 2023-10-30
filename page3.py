from tkinter import *
from tkinter import ttk

class Page3:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.root, bg="white")

        # 创建一个Text组件来显示多行文本内容
        self.text = Text(self.frame, font=("Arial", 12), wrap=WORD)
        self.text.pack()

        back_button = Button(self.frame, text="Back to Page 2", font=("Arial", 18), bg="red", command=app.show_page2)
        back_button.pack(pady=20)

    def set_file_content(self, content):
        self.text.delete(1.0, END)  # 清空Text组件的内容
        for line in content:
            self.text.insert(END, line + "\n")  # 将每行内容插入Text组件

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()
