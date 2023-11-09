from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
import os

class Page1:
    def __init__(self, app):
        self.app = app

        self.frame = Frame(app.root, bg="white")
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.file_name = None
        self.operator_name = None

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

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.grid(row=0, column=3, padx=10, pady=10)

        # Display operator name label
        self.operator_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=2, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file_path)
        self.app.page2.update_file_name(file_path)  # 调用更新文件名的方法
        self.app.page3.update_file_name(file_path)
        self.app.page4.update_file_name(file_path)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0]
        print(self.file_name)
        # 初始化两个字典
        container_data = {}
        container_weight = {}

        # 读取文件内容并处理
        with open(file_path, 'r') as file:
            lines = file.readlines() # 把每一行按照String的形式储存到lines中, lines就是一个数组
            for line in lines:
                # print(line) # 输出: [01, 01], {00000}, NAN
                line = line.strip() # 除去String开始和结尾的空白字符
                # print(line) # 去除了前后的空格还是输出: [01, 01], {00000}, NAN
                parts = line.split("}, ") # 经过这一行变成[01, 02], {00120 和 Walmart Ohio 1000 air fryers两部分
                # print(parts)
                description = parts[1] # description
                # print("description: " + description) # 成功输出: Walmart Ohio 1000 air fryers

                # 经过下面这行, [01, 02], {00120 变成 ("01", "02")元组
                # 进一步处理 coordinates，去除方括号并将元素转换为整数
                # Process coordinates
                coordinates = parts[0].split("], {")
                weight = int(coordinates[1])
                # print("Weight: ")
                # print(weight)
                coordinates[0] = coordinates[0].strip("[")
                # print(coordinates[0])

                coordinates = tuple(map(int, coordinates[0].split(", ")))
                # print("Coordinates: ")
                # print(coordinates)



                # 将坐标映射到描述
                container_data[coordinates] = description
                # print(container_data[coordinates])

                # 将描述映射到重量，但排除NAN和UNUSED
                if description != "NAN" and description != "UNUSED":
                    container_weight[description] = weight

        self.app.container_data = container_data
        self.app.container_weight = container_weight
        # print(self.app.container_data[1, 9])
        # print(self.app.container_weight["Target Cosmetics"])

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def show_file_content(self):
        # 在点击"Unloading"按钮后，将文件内容存储到Page2的file_content属性中
        self.app.page2.file_content = self.file_content
        self.app.page3.set_file_content(self.file_content)
        self.app.show_page3()

    def set_operator_name(self):
        # Use askstring to get operator name from user
        operator_name = askstring("Operator Name", "Enter Your Name:")
        if operator_name:
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")

        self.app.page2.update_operator_name(operator_name)