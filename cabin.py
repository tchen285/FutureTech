import tkinter as tk
from tkinter import messagebox

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Application")
        self.rows = 8
        self.columns = 12
        self.grid_data = [[0] * self.columns for _ in range(self.rows)]
        self.create_grid()

    def create_grid(self):
        self.buttons = [[None] * self.columns for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                button = tk.Button(self.root, width=2, height=1, bg="white",
                                   command=lambda row=i, col=j: self.toggle_color(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = button

    def toggle_color(self, row, col):
        if self.grid_data[row][col] == 0:
            self.grid_data[row][col] = 1
            self.buttons[row][col].configure(bg="black")
        else:
            self.grid_data[row][col] = 0
            self.buttons[row][col].configure(bg="white")

    def save_updates(self):
        # Save the current grid state to a file or database
        messagebox.showinfo("Save Updates", "Grid updates saved successfully.")

#if __name__ == "__main__":
    #root = tk.Tk()
    #app = GridApp(root)

    # Add a button to save updates
    # save_button = tk.Button(root, text="Save Updates", command=app.save_updates)
    # save_button.grid(row=app.rows, columnspan=app.columns, pady=10)

    root.mainloop()
