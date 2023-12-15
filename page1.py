from tkinter import *
from tkinter import filedialog
from tkinter.simpledialog import askstring  # Import askstring for input dialog
from os.path import join, expanduser
from balancing import FindBalancingPath
import os
from datetime import datetime
class Page1:

    def __init__(self, app):
        self.app = app
        self.operator_name_label = None  # This should be initialized appropriately
        self.frame = Frame(app.root, bg="white")
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        self.file_name = None
        self.operator_name = None

        logo = PhotoImage(file="logologo.png")

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

        # Add the comment button
        comment_button = Button(self.frame, text="Comment", font=("Arial", 14), bg="red", command=self.handle_comment)
        comment_button.grid(row=5, column=1, padx=10, pady=10)

        # Add a button to set operator name
        set_operator_name_button = Button(self.frame, text="Check in", font=("Arial", 14), bg="orange",
                                          command=self.set_operator_name)
        set_operator_name_button.grid(row=0, column=3, padx=10, pady=10)

        # Display operator name label
        self.operator_name_label = Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.operator_name_label.grid(row=1, column=2, padx=10, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        base_name = os.path.basename(file_path)
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, file_path)
        self.file_name = os.path.splitext(os.path.basename(file_path))[0] + "OUTBOUND.txt"
        print("((((((((((", self.file_name)
        self.app.page2.update_file_name(file_path)
        self.app.page3.update_file_name(file_path, self.file_name)
        self.app.page4.update_file_name(file_path, self.file_name)


        # 初始化两个字典
        container_data = {}
        container_weight = {}
        container_count = 0
        # 读取文件内容并处理
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split("}, ")
                description = parts[1]

                # 经过下面这行, [01, 02], {00120 变成 ("01", "02")元组
                # 进一步处理 coordinates，去除方括号并将元素转换为整数
                # Process coordinates
                coordinates = parts[0].split("], {")
                weight = int(coordinates[1])
                coordinates[0] = coordinates[0].strip("[")
                coordinates = tuple(map(int, coordinates[0].split(",")))

                # 输出坐标和描述，以确保它们被正确读取
                print("Coordinates:", coordinates)
                print("Description:", description)

                # 将坐标映射到描述
                container_data[coordinates] = description

                # 输出 container_data，以确保它被正确更新
                print("Container Data Updated:")
                print(container_data)

                if description == "NAN":
                    container_weight[description] = None

                if description == "UNUSED":
                    container_weight[description] = 0

                # 将描述映射到重量，但排除NAN和UNUSED
                if description != "NAN" and description != "UNUSED":
                    container_weight[description] = weight
                    container_count = container_count+1
                # 输出 container_weight，以确保它被正确更新
                print("Container Weight Updated:")
                print(container_weight)

        # 输出最终的 container_data 和 container_weight
        print("Final Container Data:")
        print(container_data)
        print("Final Container Weight:")
        print(container_weight)

        # 将数据赋值给 app 对象
        self.app.container_data = container_data
        self.app.container_weight = container_weight
        self.initialize_matrix()
        self.write_Manifest_log(base_name, container_count)
        # Get the desktop path
        desktop_path = join(expanduser("~"), "Desktop")

        # Generate the new filename for the outbound file on the desktop
        outbound_file_path = join(desktop_path, f"{self.file_name}")

        # self.file_name = f"{self.file_name}OUTBOUND.txt"

        # Copy the content from the original file to the outbound file with the new name
        with open(file_path, 'r') as original_file, open(outbound_file_path, 'w') as outbound_file:
            for line in original_file:
                outbound_file.write(line)

        print(f"Outbound file created on the desktop: {outbound_file_path}")

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
           # if current_operator != "":
                #self.write_to_log(current_operator, "signs out", "page1")
            # Display operator name in the label
            self.operator_name_label.config(text=f"Operator: {operator_name}")
            self.write_to_log(operator_name, "signs in")

        self.app.update_operator_name_all_pages(operator_name)

    def update_operator_name(self, name):
        self.operator_name_label.config(text=f"Operator: {name}")
        #self.app.page2.update_operator_name(name)

    def handle_comment(self):
        # Prompt the user to enter an event
        current_operator = self.operator_name_label.cget("text").replace("Operator: ", "")+ " report:"
        event_comment = askstring("Comment", "Enter the event:")
        if event_comment:
            event_comment = '"'+  event_comment+ '"'
            self.write_to_log(current_operator, event_comment)


    def write_to_log(self, txt, action):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")
        with open('log.txt', 'a') as file:
            file.write(f"{current_time} {txt} {action} \n")

    def write_Manifest_log(self,base_path,container_count):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")

        # Log the information to the log file
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{current_time} Manifest {base_path} is opened, there are {container_count} containers on the ship.\n")

        #print(f"{current_time} Manifest {file_path} is opened, there are {container_count} containers on the ship.")

    # For small test cases
    # def initialize_matrix(self):
    #     # 初始化一个2x4的矩阵，内容都是0
    #     original_matrix = [[0] * 4 for _ in range(2)]
    #     # 遍历文件内容并更新矩阵
    #     for coordinates, description in self.app.container_data.items():
    #         row, col = coordinates
    #         new_col = col - 1
    #         new_row = len(original_matrix) - row
    #         original_matrix[new_row][new_col] = self.app.container_weight.get(description, 0)
    #
    #     # 将矩阵存储到App对象中, 可以直接使用self.app.original_matrix调用
    #     self.app.original_matrix = original_matrix
    #
    #     # 输出修改后的矩阵到控制台
    #     print("\nModified Matrix:")
    #     for row in original_matrix:
    #         print(row)


    # For regular test cases
    def initialize_matrix(self):
        # 初始化一个8x12的矩阵，内容都是0
        original_matrix = [[0] * 12 for _ in range(8)]
        # 遍历文件内容并更新矩阵
        for coordinates, description in self.app.container_data.items():
            row, col = coordinates
            new_col = col - 1
            new_row = len(original_matrix) - row
            original_matrix[new_row][new_col] = self.app.container_weight.get(description, 0)

        # 将矩阵存储到App对象中, 可以直接使用self.app.original_matrix调用
        self.app.original_matrix = original_matrix
        # 输出修改后的矩阵到控制台
        print("\nModified Matrix:")
        for row in original_matrix:
            print(row)
