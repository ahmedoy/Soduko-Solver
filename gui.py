from tkinter import Tk
from tkinter import Canvas
from tkinter import simpledialog
from tkinter import messagebox
from PIL import ImageTk
import tkinter as tk
from generator import BoardGenerator
from solver import Variables, AC_3, Backtracking 
from board import Board

# Constants
WIDTH = 950
HEIGHT = 680
MARGIN = 80
SIDE_MARGIN = 30
CELL_SIZE = ((WIDTH - 2 * MARGIN) / 9) - SIDE_MARGIN
BG_IMAGE = "Sudoku_bg.png"
BUTTONS = []
INPUT_BUTTONS = []
ROW, COLUMN = -1, -1
AMOUNT_REMOVED = 0
rows, cols = 9, 9
BUTTONS = [[0] * cols for _ in range(rows)]

INPUT_BUTTONS = [0] * 9

game_board = Board()
show_hint = True
GUI_INPUT_STATE = "Solving" #Equals solving if the user's input is treated as a solution and equals "Generating" if the user's input is treated as the soduko puzzle definition
GUI_DIFFICULTY = "NONE"
MODE = 0
def show_hint_system():
    global ROW , COLUMN, show_hint
    if show_hint:
        for idx in range(81):
            ROW = idx // 9
            COLUMN = idx % 9
            available_values = game_board.get_available_values(ROW, COLUMN)
            if len(available_values) and game_board.state[idx] == "0":
                available_values_str = "\n".join([" ".join(available_values[3][i:i+3]) for i in range(0, len(available_values[3]), 3)])
                BUTTONS[COLUMN][ROW].config(text=available_values_str, font=("Helvetica", 6, "normal"))
        show_hint = False
    else:
        for idx in range(81):
            ROW = idx // 9
            COLUMN = idx % 9
            if game_board.state[idx] == "0":
                BUTTONS[COLUMN][ROW].config(text="", font=("Helvetica", 10, "normal"))
        show_hint = True


def erase_canvas():
    game_board.restart()
    canvas.delete("all")

def edit_cell(text):
    if GUI_INPUT_STATE == "Generating":
        '''Edit a cell in the board'''
        if ROW != -1 and COLUMN != -1:
            BUTTONS[ROW][COLUMN].config(text=text)
            BUTTONS[ROW][COLUMN].config(bg="#4d4d4d", font = ("Helvetica", 12, "bold"))
        for i in range(9):
            INPUT_BUTTONS[i].config(bg="#d9d9d9")
        BUTTONS[ROW][COLUMN].config(highlightthickness=0)

        if type(text) is int:
            game_board.set_idx(COLUMN, ROW, text)
        elif text.isdigit():
            game_board.set_idx(COLUMN, ROW, int(text))

    
    elif GUI_INPUT_STATE == "Solving":
        '''Edit a cell in the board'''
        if ROW != -1 and COLUMN != -1:
            BUTTONS[ROW][COLUMN].config(text=text)
        for i in range(9):
            INPUT_BUTTONS[i].config(bg="#d9d9d9")
        BUTTONS[ROW][COLUMN].config(highlightthickness=0)
        if type(text) is int:
            game_board.set_idx(COLUMN, ROW, text)
        elif text.isdigit():
            game_board.set_idx(COLUMN, ROW, int(text))

    else:
        messagebox.showinfo("Take Care", "User can't input in this mode")


def initialize_board(initial_state):
    '''Initialize board with numbers of the initial state of the game'''
    global ROW, COLUMN
    game_board.state = initial_state
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

def generate_solved_board(final_state):
    '''Generation of board after solution'''
    global ROW, COLUMN
    for i in range(len(final_state)):
        row = i // 9
        col = i % 9
        ROW = col
        COLUMN = row
        if final_state[i] != "0":
            edit_cell(final_state[i])
            BUTTONS[col][row].config(state="disabled")
            BUTTONS[col][row].config(fg="black", font = ("Helvetica", 12, "bold"))


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

def update_board(idx):
    global show_hint, GUI_INPUT_STATE
    available_values_list = game_board.get_available_values(COLUMN, ROW)
    available_values_grid = available_values_list[3]
    print(f"Game Board before = {game_board.state}")
    if str(idx) in available_values_grid:
        print("Valid Input")
        show_hint = False
        state = list(game_board.state)
        state[COLUMN * 9 + ROW] = str(idx)
        game_board.state = "".join(state)
        edit_cell(idx)
        show_hint_system()
    else:
        print("Invalid Input")
        messagebox.showinfo("Invalid Input", "This number is not valid for this cell")
    print(f"Game board After = {game_board.state}")


def create_input_buttons():
    for i in range(9):
        x = MARGIN + i * CELL_SIZE + SIDE_MARGIN
        y = HEIGHT - MARGIN + 50
        INPUT_BUTTONS[i] = tk.Button(window, text=i + 1, bg="#d9d9d9",highlightthickness=1, highlightbackground="black", fg="black", width=2, height=2, command=lambda i=i: update_board(i + 1))
        canvas.create_window(x, y, window=INPUT_BUTTONS[i])

def create_grid_buttons():
    for i in range(9):
        for j in range(9):
            x = MARGIN + i * CELL_SIZE + SIDE_MARGIN 
            y = MARGIN + j * CELL_SIZE + (1/2 * CELL_SIZE)
            BUTTONS[i][j] = tk.Button(window, text=" ", bg="#d9d9d9", fg="black", width=2, height=2, command=lambda i=i, j=j: highlight_input_buttons(i, j))
            canvas.create_window(x, y, window=BUTTONS[i][j])

def own_board_generator():
    global GUI_INPUT_STATE
    GUI_INPUT_STATE = "Generating"

def generate_board_randomly(): #AI generates a new board
    global game_board, GUI_INPUT_STATE
    game_board = BoardGenerator.generate_full_board(unique=False, amount_removed=AMOUNT_REMOVED)
    GUI_INPUT_STATE = "Generating"
    initializer(game_board.state)
    GUI_INPUT_STATE = "None"


def solved_board():
    global GUI_INPUT_STATE
    if game_board.is_empty():
        messagebox.showinfo("Take Care", "Please generate a board first")
        return
    GUI_INPUT_STATE = "Solving"
    test_board = Board()
    test_board.state = game_board.state
    test_board.display()
    vars = Variables(test_board)
    result = AC_3.AC_3(vars)
    if(result == False):
        print("Invalid Input")
        messagebox.showinfo("Invalid Input", "This board has no solution") 
        return
    result = Backtracking.Backtracking_Search(vars)
    if(result == False):
        print("Invalid Input")
        messagebox.showinfo("Invalid Input", "This board has no solution")
        return
    test_board.state = result
    generate_solved_board(test_board.state)


# def generate_board_randomly():
#     initializer(state)

def set_difficulty(difficulty):
    global GUI_DIFFICULTY, AMOUNT_REMOVED
    GUI_DIFFICULTY = difficulty
    if difficulty == "easy":
        AMOUNT_REMOVED = 30
    elif difficulty == "intermediate":
        AMOUNT_REMOVED = 40
    elif difficulty == "hard":
        AMOUNT_REMOVED = 50
    if MODE == 1:
        mode_1()
    elif MODE == 2:
        mode_2()
    elif MODE == 3:
        mode_3()

def mode_1(): #Generated and solved by AI
    global GUI_INPUT_STATE, MODE, GUI_DIFFICULTY
    MODE = 1
    GUI_INPUT_STATE = "None"
    erase_canvas()
    create_window()
    # a row of 3 buttons to choose difficulty
    if GUI_DIFFICULTY != "NONE":
        canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Solve", command=solved_board, bg="#c4bebe", fg="black", width=20))
        canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 200, window=tk.Button(window, text="Generate", command=generate_board_randomly, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//4, HEIGHT//3 + 300, window=tk.Button(window, text="Easy", command=lambda difficulty="easy": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=5))
    canvas.create_window(WIDTH- WIDTH//6.5, HEIGHT//3 + 300, window=tk.Button(window, text="Intermediate", command=lambda difficulty="intermediate": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=8))
    canvas.create_window(WIDTH- WIDTH//20.5, HEIGHT//3 + 300, window=tk.Button(window, text="Hard", command=lambda difficulty="hard": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=5))


    
def mode_2(): #Input by human and solved by AI
    global GUI_INPUT_STATE, MODE
    MODE = 2
    GUI_INPUT_STATE = "Generating"
    erase_canvas()
    create_window()
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Enter Your Own Board", command=own_board_generator, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 200, window=tk.Button(window, text="Solve", command=solved_board, bg="#c4bebe", fg="black", width=20))

    def restart_mode2():
        global GUI_INPUT_STATE, MODE
        MODE = 2
        GUI_INPUT_STATE = "Generating"
        game_board.restart()
        initializer(game_board.state)


    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 300, window=tk.Button(window, text="Erase", command=restart_mode2, bg="#c4bebe", fg="black", width=20))

                                        ##################### Interactive ################################
def generate_board_randomly_interactive():
    global game_board, GUI_INPUT_STATE, GUI_DIFFICULTY, AMOUNT_REMOVED

    
    if GUI_DIFFICULTY != "NONE":
        game_board = BoardGenerator.generate_full_board(unique=False, amount_removed=AMOUNT_REMOVED)
        GUI_INPUT_STATE = "Generating"
        initializer(game_board.state)
    canvas.create_window(WIDTH- WIDTH//4, HEIGHT//3 + 400, window=tk.Button(window, text="Easy", command=lambda difficulty="easy": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=5))
    canvas.create_window(WIDTH- WIDTH//6.5, HEIGHT//3 + 400, window=tk.Button(window, text="Intermediate", command=lambda difficulty="intermediate": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=8))
    canvas.create_window(WIDTH- WIDTH//20.5, HEIGHT//3 + 400, window=tk.Button(window, text="Hard", command=lambda difficulty="hard": set_difficulty(difficulty=difficulty), bg="#c4bebe", fg="black", width=5))


def solved_board_interactive():
    global GUI_INPUT_STATE
    GUI_INPUT_STATE = "Solving"

    if game_board.is_empty():
        messagebox.showinfo("Take Care", "Please generate a board first")
        return
    test_board = Board()
    test_board.state = game_board.state
    test_board.display()
    vars = Variables(test_board)
    result = AC_3.AC_3(vars)
    if(result == False):
        print("Invalid Input") 
        messagebox.showinfo("Invalid Input", "This board has no solution")
        return
    result = Backtracking.Backtracking_Search(vars)
    if(result == False):
        print("Invalid Input")
        messagebox.showinfo("Invalid Input", "This board has no solution")
        return
    test_board.state = result

    
def mode_3(): #AI generated or Human input board and solved interactively
    global GUI_INPUT_STATE, MODE
    MODE = 3
    GUI_INPUT_STATE = "Generating"
    erase_canvas()
    create_window()
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 300, window=tk.Button(window, text="Solve", command=solved_board_interactive, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 200, window=tk.Button(window, text="Generate Board Randomly", command=generate_board_randomly_interactive, bg="#c4bebe", fg="black", width=20))
    canvas.create_window(WIDTH- WIDTH//6, HEIGHT//3 + 100, window=tk.Button(window, text="Enter Your Own Board", command=mode_3, bg="#c4bebe", fg="black", width=20))
    




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