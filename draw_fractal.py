import os
import inspect
from sys import argv

from matplotlib.pyplot import draw
import fractal
from tkinter import *
from PIL import Image, ImageDraw, ImageTk, Image


# This file is run only
if __name__ == '__main__':

    def test():
        pass

    def draw_fractal(width: int, height: int, iterations: int,
                     x_min: float, x_max: float, y_min: float, y_max: float):
        """This method returns a PIL image of the given fractal.
        
        :param width: The height of the image in pixels
        :param height: The width of the image in pixels
        :param iterations: The number of iterations to draw the fractal to
        :return Image: A PIL image object of the fractal
        """

        # Create the window
        im = Image.new('HSV', (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(im)

        # For every pixel, find the corresponding value of the fractal
        for x in range(0, width):
            for y in range(0, height):

                # Convert pixel coordinate to complex number
                c = complex(x_min + (x / width) * (x_max - x_min),
                            y_min + (y / height) * (y_max - y_min))

                # Compute the number of iterations
                m = fractal.mandelbrot(c, iterations)

                # Find the color of the pixel
                hue = int(255 * m / iterations)
                saturation = 255
                value = 255 if m < iterations else 0

                # Plot the point
                draw.point([x, y], (hue, saturation, value))

        # Set the image to rgb mode
        im = im.convert('RGB')

        # Return the drawn fractal
        return ImageTk.PhotoImage(im)

    # region Window Initialization

    # Create the window
    window = Tk()

    # Set window size
    window_width = 1000
    window_height = 800
    window.geometry(f"{window_width}x{window_height}")

    # Set the window title
    window.title('Fractal Viewer')

    # Create a menu bar
    menu = Menu(window)

    # Create a dropdown menu of fractals to display
    fractal_menu = Menu(menu, tearoff=0)

    # Add each fractal to the dropdown
    for frac in inspect.getmembers(fractal, inspect.isfunction):
        fractal_menu.add_command(label=frac[0].capitalize(), command=test)

    # Add the fractal dropdown to the menu
    menu.add_cascade(label="Fractal", menu=fractal_menu)
    
    # Create a dropdown menu of color pallets for the fractals
    color_menu = Menu(menu, tearoff=0)

    # Add each color to the dropdown
    for color in ['red', 'green', 'blue']:
        color_menu.add_command(label=color.capitalize(), command=test)

    # Add the color dropdown to the menu
    menu.add_cascade(label="Color Palette", menu=color_menu)

    # Register the dropdown to the root
    window.config(menu=menu)

    # The fractal image variable
    fractal_image = None

    # Create the fractal display
    fractal_display = Frame(window, width=window_width, height=window_height)
    fractal_display.pack()
    fractal_display.place(anchor='center', relx=0.5, rely=0.5)

    # Place the fractal display inside a label
    fractal_display_label = Label(fractal_display, image=fractal_image)
    fractal_display_label.pack()  

    # endregion Window Initialization

    # region Controls

    # The zoom and initial position of the camera on the fractal image
    zoom = 1
    position = (0, 0)

    def get_bounds():
        """Returns the x and y draw boundaries from the zoom and position"""
        global zoom, position

    # Define a scrollwheel function
    def _on_scroll(self, event):
        """This function is called every tick the user scrolls. This will zoom in our out
        on the fractal.
        """
        global zoom

        # Zoom the camera
        zoom += zoom * 0.1 * event.delta

        # Update the fractal
        draw_fractal()

    # Bind the scrollwheel function
    window.bind_all("<MouseWheel>", _on_scroll)

    # Update the fractal display
    fractal_image = draw_fractal(window_width, window_height, 80,
                                 -2, 1, -1, 1)

    # endregion Controls

    # Run the window
    window.mainloop()