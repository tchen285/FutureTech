from tkinter import *
from page1 import Page1
from page2 import Page2
from page3 import Page3
from page4 import Page4
from show_balance_cost_page import ShowBalanceCost
from show_description_page import ShowDescriptions
from show_load_unload_cost_page import ShowLoadUnloadCost
from show_load_unload_page import ShowLoadUnload

class ShipManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ship Management System")
        self.root.config(padx=20, pady=20, bg="white")

        self.balance_list = []
        # Initialization matrix
        self.original_matrix = None

        # Initialization page
        self.page1 = Page1(self)
        self.page2 = Page2(self)
        self.page3 = Page3(self)
        self.page4 = Page4(self)
        self.balance_cost_page = ShowBalanceCost(self)
        self.description_page = ShowDescriptions(self)
        self.load_unload_page = ShowLoadUnloadCost(self)
        self.show_load_unload_page = ShowLoadUnload(self)

        # Initialize two dictionaries
        self.container_data = {}   # self.container_data[coordinate] = description
        self.container_weight = {} # self.container_weight[description] = weight

        self.show_page1()

    def show_page1(self):
        self.page2.hide()
        self.page3.hide()
        self.page1.show()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_page2(self):
        self.page1.hide()
        self.page2.show()
        self.page3.hide()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_page3(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.show()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_page4(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.hide()
        self.page4.show()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_balance_cost_page(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        self.balance_cost_page.show()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_description_page(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.show()
        self.load_unload_page.hide()
        self.show_load_unload_page.hide()

    def show_load_unload_cost_page(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.show()
        self.show_load_unload_page.hide()

    def show_load_unload_page(self):
        self.page1.hide()
        self.page2.hide()
        self.page3.hide()
        self.page4.hide()
        self.balance_cost_page.hide()
        self.description_page.hide()
        self.load_unload_page.hide()
        self.show_load_unload_page.show()

    def update_operator_name_all_pages(self, name):
        self.page1.update_operator_name(name)
        self.page2.update_operator_name(name)
        self.page3.update_operator_name(name)
        self.page4.update_operator_name(name)
        self.balance_cost_page.update_operator_name(name)
        self.description_page.update_operator_name(name)
        self.load_unload_page.update_operator_name(name)
        self.show_load_unload_page.update_operator_name(name)

if __name__ == "__main__":
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry("1300x800")
    app = ShipManagementApp(root)
    root.mainloop()