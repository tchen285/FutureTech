from tkinter import *
from page1 import Page1
from page2 import Page2
from page3 import Page3
# 以下内容是测试内容, 测试用python字典的形式实现txt文件字典的转换
class ShipManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ship Management System")
        self.root.config(padx=20, pady=20, bg="white")

        # 初始化页面
        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)

        # 初始化两个字典
        self.container_data = {}
        self.container_weight = {}

        self.show_page1()

    def show_page1(self):
        self.page2.hide()
        self.page3.hide()
        self.page1.show()

    def show_page2(self):
        self.page1.hide()
        self.page2.show()
        self.page3.hide()

    def show_page3(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.show()

if __name__ == "__main__":
    root = Tk()
    app = ShipManagementApp(root)
    root.mainloop()
