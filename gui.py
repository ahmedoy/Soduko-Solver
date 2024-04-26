from tkinter import Tk
from tkinter import Canvas
from tkinter import simpledialog
from tkinter import messagebox
from PIL import ImageTk
import tkinter as tk
from generator import BoardGenerator

# Constants
WIDTH = 950
HEIGHT = 680
MARGIN = 80
SIDE_MARGIN = 30
CELL_SIZE = ((WIDTH - 2 * MARGIN) / 9) - SIDE_MARGIN
BG_IMAGE = "Sudoku_bg.png"
BUTTONS = []
INPUT_BUTTONS = []
ROW, COLUMN = 0, 0

rows, cols = 9, 9
BUTTONS = [[0] * cols for _ in range(rows)]

INPUT_BUTTONS = [0] * 9

new_board = BoardGenerator.generate_full_board(unique=False, amount_removed=30)
state = new_board.state

def show_hint_system():
    pass

def erase_canvas():
    canvas.delete("all")

def edit_cell(text):
    '''Edit a cell in the board'''
    if ROW != -1 and COLUMN != -1:
         BUTTONS[ROW][COLUMN].config(text=text)
    for i in range(9):
        INPUT_BUTTONS[i].config(bg="#d9d9d9")
    BUTTONS[ROW][COLUMN].config(highlightthickness=0)


def initialize_board(initial_state):
    '''Initialize board with numbers of the initial state of the game'''
    global ROW, COLUMN
    for i in range(len(initial_state)):
        row = i // 9
        col = i % 9
        ROW = col
        COLUMN = row
        if initial_state[i] != "0":
            edit_cell(initial_state[i])
            BUTTONS[col][row].config(state="disabled")
            BUTTONS[col][row].config(bg="#4d4d4d", font = ("Helvetica", 12, "bold"))
        else:
            edit_cell("")
            BUTTONS[col][row].config(state="normal")
            BUTTONS[col][row].config(bg="#d9d9d9", font = ("Helvetica", 10, "normal"))

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
    create_input_buttons()

def initializer(board_state):
    global ROW, COLUMN
    initialize_board(board_state)
    ROW, COLUMN = -1, -1

def create_window():
    create_grid()
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3, window=tk.Button(window, text="HINT", command=show_hint_system, bg="#c4bebe", fg="black", width=20))

def change_highlights():
    BUTTONS[ROW][COLUMN].config(highlightthickness = 0)

def highlight_input_buttons(row, column):
    global ROW 
    global COLUMN 
    if ROW != row or COLUMN!= column:
        change_highlights()
    ROW = row
    COLUMN = column
    for i in range(9):
        INPUT_BUTTONS[i].config(bg="#dc8a89")
    BUTTONS[ROW][COLUMN].config(highlightthickness=2, highlightbackground="black")

def create_input_buttons():
    for i in range(9):
        x = MARGIN + i * CELL_SIZE + SIDE_MARGIN
        y = HEIGHT - MARGIN + 50
        INPUT_BUTTONS[i] = tk.Button(window, text=i + 1, bg="#d9d9d9",highlightthickness=1, highlightbackground="black", fg="black", width=2, height=2, command=lambda i=i: edit_cell(i + 1))
        canvas.create_window(x, y, window=INPUT_BUTTONS[i])

def create_grid_buttons():
    for i in range(9):
        for j in range(9):
            x = MARGIN + i * CELL_SIZE + SIDE_MARGIN 
            y = MARGIN + j * CELL_SIZE + (1/2 * CELL_SIZE)
            BUTTONS[i][j] = tk.Button(window, text=" ", bg="#d9d9d9", fg="black", width=2, height=2, command=lambda i=i, j=j: highlight_input_buttons(i, j))
            canvas.create_window(x, y, window=BUTTONS[i][j])

def own_board_generator():
    USER_INP = simpledialog.askstring(title="Board",
                                  prompt="Enter Your Board Row by ROW :)")
    if USER_INP:
        if len(USER_INP) == 9*9:
            initializer(USER_INP)
        else:
            messagebox.showinfo("Take Care", "The state isn't 9x9")

def generate_solved_board():
    pass 

def generate_board_randomly():
    initializer(state)

def mode_1(): #Generated and solved by AI
    erase_canvas()
    create_window()
    initializer(state)
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Solve", command=generate_solved_board, bg="#c4bebe", fg="black", width=20))

    
def mode_2(): #Input by human and solved by AI
    erase_canvas()
    create_window()
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Enter Your Own Board", command=own_board_generator, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 200, window=tk.Button(window, text="Solve", command=generate_solved_board, bg="#c4bebe", fg="black", width=20))

def mode_3(): #AI generated or Human input board and solved interactively
    erase_canvas()
    create_window()
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 200, window=tk.Button(window, text="Generate Board Randomly", command=generate_board_randomly, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Enter Your Own Board", command=own_board_generator, bg="#c4bebe", fg="black", width=20))


    ### interactive here!!!!!!!!


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