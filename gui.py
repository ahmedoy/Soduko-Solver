from tkinter import Tk
from tkinter import Canvas
from tkinter import Image
from PIL import ImageTk
import tkinter as tk
# Constants
WIDTH = 950
HEIGHT = 680
MARGIN = 80
SIDE_MARGIN = 30
CELL_SIZE = ((WIDTH - 2 * MARGIN) / 9) -SIDE_MARGIN
BG_IMAGE = "Sudoku_bg.png"

def erase_canvas():
    canvas.delete("all")
    
def create_grid():
    # Create a 9x9 grid
    for i in range(10):
        color = "black" if i % 3 == 0 else "gray"
        #vertical lines
        x0 = MARGIN + i * CELL_SIZE 
        y0 = MARGIN
        x1 = MARGIN + i * CELL_SIZE 
        y1 = HEIGHT - MARGIN
        canvas.create_line(x0, y0, x1, y1, fill=color)
        
        #horizontal lines
        x0 = MARGIN
        y0 = MARGIN + i * CELL_SIZE
        x1 = WIDTH - MARGIN - (SIDE_MARGIN * 9)
        y1 = MARGIN + i * CELL_SIZE 
        canvas.create_line(x0, y0, x1, y1, fill=color)
        print("Ana hena")
    create_grid_buttons()

def create_grid_buttons():
    for i in range(9):
        for j in range(9):
            x = MARGIN + i * CELL_SIZE + SIDE_MARGIN 
            y = MARGIN + j * CELL_SIZE + (1/2 * CELL_SIZE)
            canvas.create_window(x, y, window=tk.Button(window, text="1", bg="#c4bebe", fg="black", width=2, height=2))
            

     
def mode_1():
    erase_canvas()
    create_grid()
    
    


def mode_2():
    erase_canvas()
    create_grid()

def mode_3():
    erase_canvas()
    create_grid()


# Create the main window
window = Tk()
window.title("Suduko Solver")
window.resizable(False, False)

#Create a background image
canvas = Canvas(window, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

img_path = "Sudoku_bg.png"
background_img = ImageTk.PhotoImage(file = BG_IMAGE)
canvas.create_image(0,0, anchor='nw', image=background_img)

#Create buttons 
mode_1_button = canvas.create_window(WIDTH//2, HEIGHT//3, window=tk.Button(window, text="Mode 1", command=mode_1, bg="#c4bebe", fg="black"))
mode_2_button = canvas.create_window(WIDTH//2, HEIGHT//3 + 100, window=tk.Button(window, text="Mode 2", command=mode_2, bg="#c4bebe", fg="black"))
mode_3_button = canvas.create_window(WIDTH//2, HEIGHT//3 + 200, window=tk.Button(window, text="Mode 3", command=mode_3, bg="#c4bebe", fg="black"))


window.mainloop()