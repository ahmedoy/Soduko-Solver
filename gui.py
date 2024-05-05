from tkinter import Tk
from tkinter import Canvas
from tkinter import simpledialog
from tkinter import messagebox
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
import tkinter as tk
from generator import BoardGenerator
from solver import Variables, AC_3, Backtracking 
from board import Board
from time import time
from collections import deque

BUTTON_COLOR = "#FFC374"


class BoardGUI(tk.Frame):

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.width = 950
        self.height = 680
        self.margin = 80
        self.side_margin = 30
        self.cell_size = ((self.width - 2 * self.margin) / 9) - self.side_margin
        self.canvas = Canvas(self.root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.BG_image = "sudoko.jpg"
        self.board_rows, self.board_columns = 9, 9
        self.buttons = [[0] * self.board_columns for _ in range(self.board_rows)]
        self.input_buttons = [0] * 9
        self.row_idx, self.column_idx = -1, -1
        self.prev_cell_stack = deque()
        self.amount_removed = 0
        self.undo_stack = deque()


        self.game_board = Board()
        self.showHint = True
        self.GUI_INPUT_STATE = "Solving" #Equals solving if the user's input is treated as a solution and equals "Generating" if the user's input is treated as the soduko puzzle definition
        self.GUI_DIFFICULTY = "NONE"
        self.mode = 0
        self.return_to_menu()

    def generate_solved_board(self,final_state):
        '''Generation of board after solution'''
        for i in range(len(final_state)):
            row = i // 9
            col = i % 9
            self.row_idx = col
            self.column_idx = row
            if final_state[i] != "0":
                self.edit_cell(final_state[i])
                self.buttons[col][row].config(state="disabled")
                self.buttons[col][row].config(fg="black", font = ("Helvetica", 12, "bold"))

    def solved_board(self):
        if self.game_board.is_empty():
            messagebox.showinfo("Take Care", "Please generate a board first")
            return
        self.GUI_INPUT_STATE = "Solving"
        test_board = Board()
        test_board.state = self.game_board.state
        test_board.display()
        vars = Variables(test_board)
        start = time()
        result = AC_3.AC_3(vars)
        if(result == False):
            print("Invalid Input")
            messagebox.showinfo("Invalid Input", "This board has no solution") 
            return
        result = Backtracking.Backtracking_Search(vars) #backtracking used for checking validity of the board and solving it
        end = time()
        print(f"Time taken to solve board in {self.GUI_DIFFICULTY} level = {end - start}")

        if(result == False):
            print("Invalid Input")
            messagebox.showinfo("Invalid Input", "This board has no solution")
            return
        test_board.state = result
        self.generate_solved_board(test_board.state)

    def change_highlights(self):
        self.buttons[self.row_idx][self.column_idx].config(highlightthickness = 0)

    def highlight_input_buttons(self,row, column):

        if self.row_idx != row or self.column_idx!= column:
            self.change_highlights()
        self.row_idx = row
        self.column_idx = column
        for i in range(9):
            self.input_buttons[i].config(bg="#dc8a89")
        self.buttons[self.row_idx][self.column_idx].config(highlightthickness=2, highlightbackground="black")

    def update_board(self,idx):
    
        available_values_list = self.game_board.get_available_values(self.column_idx, self.row_idx)
        available_values_grid = available_values_list[3]
        if str(idx) in available_values_grid:
            print("Valid Input")
            self.showHint = False
            state = list(self.game_board.state)
            state[self.column_idx * 9 + self.row_idx] = str(idx)
            self.undo_stack.append((self.game_board.state, self.column_idx, self.row_idx))
            self.game_board.state = "".join(state)
            self.edit_cell(idx)
            self.show_hint_system()
        else:
            print("Invalid Input")
            messagebox.showinfo("Invalid Input", "This number is not valid for this cell")

    def edit_cell(self,text):
        if self.GUI_INPUT_STATE == "Generating":
            '''Edit a cell in the board'''
            if self.row_idx != -1 and self.column_idx != -1:
                self.buttons[self.row_idx][self.column_idx].config(text=text)
                self.buttons[self.row_idx][self.column_idx].config(bg="#4d4d4d", font = ("Helvetica", 12, "bold"))
            for i in range(9):
                self.input_buttons[i].config(bg=BUTTON_COLOR)
            self.buttons[self.row_idx][self.column_idx].config(highlightthickness=0)

            if type(text) is int:
                self.game_board.set_idx(self.column_idx, self.row_idx, text)
            elif text.isdigit():
                self.game_board.set_idx(self.column_idx, self.row_idx, int(text))

        
        elif self.GUI_INPUT_STATE == "Solving":
            if self.row_idx != -1 and self.column_idx != -1:
                self.buttons[self.row_idx][self.column_idx].config(text=text)
            for i in range(9):
                self.input_buttons[i].config(bg=BUTTON_COLOR)
            self.buttons[self.row_idx][self.column_idx].config(highlightthickness=0, font=("Helvetica", 12, "normal"), fg="green")
            if type(text) is int:
                self.game_board.set_idx(self.column_idx, self.row_idx, text)
            elif text.isdigit():
                self.game_board.set_idx(self.column_idx, self.row_idx, int(text))

        else:
            messagebox.showinfo("Take Care", "User can't input in this mode")

    def erase_canvas(self):
        self.game_board.restart()
        self.canvas.delete("all")

    def update_board(self,idx):
        available_values_list = self.game_board.get_available_values(self.column_idx, self.row_idx)
        available_values_grid = available_values_list[3]
        if str(idx) in available_values_grid:
            print("Valid Input")
            self.showHint = False
            state = list(self.game_board.state)
            state[self.column_idx * 9 + self.row_idx] = str(idx)
            self.undo_stack.append((self.game_board.state, self.column_idx, self.row_idx))
            self.game_board.state = "".join(state)
            self.edit_cell(idx)
            self.show_hint_system()
        else:
            print("Invalid Input")
            messagebox.showinfo("Invalid Input", "This number is not valid for this cell")

    def create_input_buttons(self):
        for i in range(9):
            x = self.margin + i * self.cell_size + self.side_margin
            y = self.height - self.margin + 50
            self.input_buttons[i] = tk.Button(self.root, text=i + 1, bg=BUTTON_COLOR,highlightthickness=1, highlightbackground="black", fg="black", width=2, height=2, command=lambda i=i: self.update_board(i + 1))
            self.canvas.create_window(x, y, window=self.input_buttons[i])

    def create_grid_buttons(self):
        for i in range(9):
            for j in range(9):
                x = self.margin + i * self.cell_size + self.side_margin 
                y = self.margin + j * self.cell_size + (1/2 * self.cell_size)
                self.buttons[i][j] = tk.Button(self.root, text=" ", bg="#F6F1EE", fg="black", width=2, height=2, command=lambda i=i, j=j: self.highlight_input_buttons(i, j))
                self.canvas.create_window(x, y, window=self.buttons[i][j])

    def create_grid(self):
        # Create a 9x9 grid

        for i in range(10):
            color = "black" if i % 3 == 0 else "gray"
            #vertical lines
            x0 = self.margin + i * self.cell_size 
            y0 = self.margin
            x1 = self.margin + i * self.cell_size 
            y1 = self.height - self.margin
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            
            #horizontal lines
            x0 = self.margin
            y0 = self.margin + i * self.cell_size
            x1 = self.width - self.margin - (self.side_margin * 9)
            y1 = self.margin + i * self.cell_size 
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
        self.create_grid_buttons()
        self.create_input_buttons()

    def create_window(self):
        self.create_grid()
        # change the color of the background
        self.canvas.config(bg="#FFF7E9")
        self.canvas.create_window(self.width- self.width//6, self.height//3, window=tk.Button(self.root, text="HINT", command=self.show_hint_system, bg=BUTTON_COLOR, fg="black", width=20))
        self.canvas.create_window(self.width- self.width//6, self.height//3 - 100, window=tk.Button(self.root, text="Return to Home", command=self.return_to_menu, bg=BUTTON_COLOR, fg="black", width=20))

    def show_background(self):
        background_img = Image.open(self.BG_image)
        resized_img = background_img.resize((self.width, self.height))
        self.background_photo = ImageTk.PhotoImage(resized_img)
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_photo)
        
    def show_hint_system(self):
        if self.showHint:
            for idx in range(81):
                self.row_idx = idx // 9
                self.column_idx = idx % 9
                available_values = self.game_board.get_available_values(self.row_idx, self.column_idx)
                if len(available_values) and self.game_board.state[idx] == "0":
                    available_values_str = "\n".join([" ".join(available_values[3][i:i+3]) for i in range(0, len(available_values[3]), 3)])
                    self.buttons[self.column_idx][self.row_idx].config(text=available_values_str, font=("Helvetica", 6, "normal"))
            self.showHint = False
        else:
            for idx in range(81):
                self.row_idx = idx // 9
                self.column_idx = idx % 9
                if self.game_board.state[idx] == "0":
                    self.buttons[self.column_idx][self.row_idx].config(text="", font=("Helvetica", 10, "normal"))
            self.showHint = True
    def show_hint(self):
        if self.showHint:
            for idx in range(81):
                self.row = idx // 9
                self.column_idx = idx % 9
                available_values = self.game_board.get_available_values(self.row, self.column_idx)
                if len(available_values) and self.game_board.state[idx] == "0":
                    available_values_str = "\n".join([" ".join(available_values[3][i:i+3]) for i in range(0, len(available_values[3]), 3)])
                    self.buttons[self.column_idx][self.row].config(text=available_values_str, font=("Helvetica", 6, "normal"))
            self.showHint = False
        else:
            for idx in range(81):
                self.row = idx // 9
                self.column_idx = idx % 9
                if self.game_board.state[idx] == "0":
                    self.buttons[self.column_idx][self.row].config(text="", font=("Helvetica", 10, "normal"))
            self.showHint = True

    def erase_canvas(self):
        self.game_board.restart()
        self.canvas.delete("all")

    def set_difficulty(self,difficulty):
        self.GUI_DIFFICULTY = difficulty
        if difficulty == "easy":
            self.amount_removed = 30
        elif difficulty == "intermediate":
            self.amount_removed = 40
        elif difficulty == "hard":
            self.amount_removed = 50
        if self.mode == 1:
            self.mode_1()
        elif self.mode == 2:
            self.mode_2()

    
    def is_valid_row(self,row):
        # Check for duplicates
        #print(type(row))
        if (type(row) == str):
            row = ''.join([char for char in row if char != '0'])
    
        if (type(row) == list):
            row = list(filter(lambda x: x != '0', row))
        
        if len(row) != len(set(row)):
            return False
        
        return True
    
    def is_valid_board(self,board):
        # Check each row
        for i in range(9):
            row = board[i * 9: (i + 1) * 9]
            if not self.is_valid_row(row):
                return False

        # Check each column
        for i in range(9):
            column = [board[j * 9 + i] for j in range(9)]
            if not self.is_valid_row(column):
                return False

        # Check each 3x3 subgrid
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [board[x + y * 9] for x in range(3) for y in range(3)]
                if not self.is_valid_row(subgrid):
                    return False

        return True
    def initializer(self,board_state):

        self.initialize_board(board_state)
        print(f"Previous Row = {self.row_idx}, Previous Column = {self.column_idx}")
        self.row_idx, self.column_idx = -1, -1

    def initialize_board(self,initial_state):
        '''Initialize board with numbers of the initial state of the game'''
        self.game_board.state = initial_state
        for i in range(len(initial_state)):
            row = i // 9
            col = i % 9
            self.row_idx = col
            self.column_idx = row
            if initial_state[i] != "0":
                self.edit_cell(initial_state[i])
                self.buttons[col][row].config(state="disabled")
                self.buttons[col][row].config(bg="#4d4d4d", font = ("Helvetica", 12, "bold"))
            else:
                self.edit_cell("")
                self.buttons[col][row].config(state="normal")
                self.buttons[col][row].config(bg="#d9d9d9", font = ("Helvetica", 10, "normal"))

    def own_board_generator(self):

        self.GUI_INPUT_STATE = "Generating"
        USER_INP = simpledialog.askstring(title="Board",
                                    prompt="Enter Your Board Row by Row :)")
        if USER_INP:
            if len(USER_INP) != 9*9:
                messagebox.showinfo("Take Care", "Invalid.The state isn't 9x9")

            elif not self.is_valid_board(USER_INP):
                messagebox.showinfo("Take Care", "Invalid Board")
            
            elif len(USER_INP) == 9*9 and self.is_valid_board(USER_INP):
                self.initializer(USER_INP)

    def generate_board_randomly(self): #AI generates a new board
        start = time()
        game_board = BoardGenerator.generate_full_board(unique=True, amount_removed=self.amount_removed)
        end = time()
        print(f"Time taken to generate board in {self.GUI_DIFFICULTY} level = {end - start}")
        self.GUI_INPUT_STATE = "Generating"
        self.initializer(game_board.state)
        self.GUI_INPUT_STATE = "None"

    def undo(self):
        if len(self.undo_stack) == 0:
            messagebox.showinfo("Take Care", "No more undos")
        else:
            self.game_board.state, col, row = self.undo_stack.pop()

            print(f"Game board after undo = {self.game_board.state}")
            self.initializer(self.game_board.state)
            #BUTTONS[PREV_ROW][PREV_COLUMN].config(highlightthickness=0, font=("Helvetica", 12, "normal"), fg="blue", bg="#d9d9d9")
            self.GUI_INPUT_STATE = "Solving"

    def set_difficulty_interactive(self,difficulty):
        if difficulty == "easy":
            self.amount_removed = 30
        elif difficulty == "intermediate":
            self.amount_removed = 40
        elif difficulty == "hard":
            self.amount_removed = 50
        game_board = BoardGenerator.generate_full_board(unique=False, amount_removed=self.amount_removed)
        self.GUI_INPUT_STATE = "Generating"
        self.initializer(game_board.state)
                                            
    def generate_board_randomly_interactive(self):


        self.canvas.create_window(self.width- self.width//4, self.height//3 + 370, window=tk.Button(self.root, text="Easy", command=lambda difficulty="easy": self.set_difficulty_interactive(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=5))
        self.canvas.create_window(self.width- self.width//6.5, self.height//3 + 370, window=tk.Button(self.root, text="Intermediate", command=lambda difficulty="intermediate": self.set_difficulty_interactive(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=8))
        self.canvas.create_window(self.width- self.width//20.5, self.height//3 + 370, window=tk.Button(self.root, text="Hard", command=lambda difficulty="hard": self.set_difficulty_interactive(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=5))


    def solved_board_interactive(self):


        if self.game_board.is_empty():
            messagebox.showinfo("Take Care", "Please generate a board first")
            return
        test_board = Board()
        test_board.state = self.game_board.state
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
        self.GUI_INPUT_STATE = "Solving"
        test_board.state = result

    def mode_1(self):
        self.mode = 1
        self.GUI_INPUT_STATE = "None"
        self.erase_canvas()
        self.create_window()
        # a row of 3 buttons to choose difficulty
        if self.GUI_DIFFICULTY != "NONE":
            self.canvas.create_window(self.width- self.width//6, self.height//3 + 100, window=tk.Button(self.root, text="Solve", command=self.solved_board, bg=BUTTON_COLOR, fg="black", width=20))
            self.canvas.create_window(self.width- self.width//6, self.height//3 + 200, window=tk.Button(self.root, text="Generate", command=self.generate_board_randomly, bg=BUTTON_COLOR, fg="black", width=20))
        self.canvas.create_window(self.width- self.width//4, self.height//3 + 300, window=tk.Button(self.root, text="Easy", command=lambda difficulty="easy": self.set_difficulty(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=5))
        self.canvas.create_window(self.width- self.width//6.5, self.height//3 + 300, window=tk.Button(self.root, text="Intermediate", command=lambda difficulty="intermediate": self.set_difficulty(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=8))
        self.canvas.create_window(self.width- self.width//20.5, self.height//3 + 300, window=tk.Button(self.root, text="Hard", command=lambda difficulty="hard": self.set_difficulty(difficulty=difficulty), bg=BUTTON_COLOR, fg="black", width=5))

    def mode_2(self):

        self.mode = 2
        self.GUI_INPUT_STATE = "Generating"
        self.erase_canvas()
        self.create_window()
        self.canvas.create_window(self.width- self.width//6, self.height//3 + 100, window=tk.Button(self.root, text="Enter Your Own Board", command=self.own_board_generator, bg=BUTTON_COLOR, fg="black", width=20))
        self.canvas.create_window(self.width- self.width//6, self.height//3 + 200, window=tk.Button(self.root, text="Solve", command=self.solved_board, bg=BUTTON_COLOR, fg="black", width=20))

        def restart_mode2():

            self.mode = 2
            self.GUI_INPUT_STATE = "Generating"
            self.game_board.restart()
            self.initializer(self.game_board.state)


        self.canvas.create_window(self.width- self.width//6, self.height//3 + 300, window=tk.Button(self.root, text="Erase", command=restart_mode2, bg=BUTTON_COLOR, fg="black", width=20))

    def mode_3(self):

        self.mode = 3
        self.GUI_INPUT_STATE = "Generating"
        self.erase_canvas()
        self.create_window()
        self.canvas.create_window(self.width- self.width//4, self.height//3 + 420, window=tk.Button(self.root, text="Undo", command=self.undo, bg=BUTTON_COLOR, fg="black", width=5))
        self.canvas.create_window(self.width- self.width//6, self.height//3 + 300, window=tk.Button(self.root, text="Solve", command=self.solved_board_interactive, bg=BUTTON_COLOR, fg="black", width=20))
        self.canvas.create_window(self.width- self.width//6, self.height//3 + 200, window=tk.Button(self.root, text="Generate Board Randomly", command=self.generate_board_randomly_interactive, bg=BUTTON_COLOR, fg="black", width=20))
        self.canvas.create_window(self.width- self.width//6, self.height//3 + 100, window=tk.Button(self.root, text="Enter Your Own Board", command=self.own_board_generator, bg=BUTTON_COLOR, fg="black", width=20))
    


    def show_menu(self):
        #Create buttons 
        style = ThemedStyle(self.root)
        style.set_theme("arc")
        style.configure("TButton", font=("Helvetica", 12, "bold"))
        self.canvas.create_window(self.width//2, self.height//3, window=tk.Button(self.root, text="Mode 1", command=self.mode_1, bg=BUTTON_COLOR, fg="brown"))
        self.canvas.create_window(self.width//2, self.height//3 + 100, window=tk.Button(self.root, text="Mode 2", command=self.mode_2, bg=BUTTON_COLOR, fg="brown"))
        self.canvas.create_window(self.width//2, self.height//3 + 200, window=tk.Button(self.root, text="Mode 3", command=self.mode_3, bg=BUTTON_COLOR, fg="brown"))
    def return_to_menu(self):
        self.erase_canvas()
        self.show_menu()
        self.show_background()





__main__ = True

if __main__:
    root = Tk()
    app = BoardGUI(root)
    root.mainloop()
