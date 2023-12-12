from tkinter import Tk, Canvas, Button, filedialog
import os


class VirtualSquaresApp:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Virtual Squares")
        self.root.geometry("800x600")

        self.file_path = file_path

        # Create a canvas to draw on
        self.canvas = Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()

        # Example: Draw a virtual square at position (100, 100) with a side length of 50
        self.draw_virtual_square(100, 100, 50)

        # Add a button to trigger the virtual squares drawing
        draw_squares_button = Button(self.root, text="Draw Virtual Squares", command=self.draw_virtual_squares)
        draw_squares_button.pack()

    def draw_virtual_square(self, x, y, side_length):
        # Draw a rectangle using the canvas create_rectangle method
        self.canvas.create_rectangle(
            x, y, x + side_length, y + side_length,
            outline="black", width=2, fill="lightblue"
        )

    def draw_virtual_squares(self):
        # Clear the canvas before drawing new squares
        self.canvas.delete("all")

        # Read the content of the selected file and extract information for drawing
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                parts = line.split("}, ")
                coordinates = parts[0].split("], {")
                coordinates = tuple(map(int, coordinates[0].strip("[").split(",")))

                # Draw a virtual square based on the coordinates
                self.draw_virtual_square(coordinates[0], coordinates[1], 30)  # Adjust side_length as needed


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    app = VirtualSquaresApp(Tk(), file_path)
    app.root.mainloop()


if __name__ == "__main__":
    browse_file()
