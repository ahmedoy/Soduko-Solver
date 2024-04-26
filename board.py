class Board:
    rows = 9
    columns = 9
    empty_slot = "0"
    value_domain = (1,2,3,4,5,6,7,8,9)
    def __init__(self):
        self.state = self.empty_slot * (self.rows * self.columns) #initially board state is fully blank

    def check_game_end(self):
        return BoardLogic.check_game_end(self.state)
    
    def get_idx(self, i:int , j:int): # Returns value at index i,j
        return BoardLogic.get_idx(self.state, i, j)
    
    def set_idx_val(self, i:int, j:int, value: int): # Sets the value at position i,j in the board but also does certain validations first
        if self.get_idx(i, j) != self.empty_slot:
            return
        if BoardLogic.check_valid_move(self.state, i, j, value): #Checks if the value to be inserted satisfies all constraints
            self.state = BoardLogic.set_idx(self.state, i , j, value)
    
    def set_idx(self, i:int, j:int, value: int): # Sets the value at position i,j in the board without any validations
        self.state = BoardLogic.set_idx(self.state, i , j, value)

    def display(self):
        BoardLogic.display_board2(self.state)

    def display2(self):
        BoardLogic.display_board2(self.state)

    def get_available_values(self, row, column):
        if self.get_idx(row, column) != self.empty_slot:
            return self.get_idx(row, column) #If the variable is assigned just return its value
        
        #If it's not assigned return the values it can take according to different constraints
        available_row = [str(i) for i in self.value_domain]
        available_column = [str(i) for i in self.value_domain]
        available_grid = [str(i) for i in self.value_domain]
        available_all = None

        #Positions Related by row constraint
        for col_2 in range(Board.columns):            
            value = self.get_idx(row, col_2)
            if value != self.empty_slot:
                available_row.remove(value)

        #Positions Related by column constraint
        for row_2 in range(Board.rows):            
            value = self.get_idx(row_2, column)            
            if value != self.empty_slot:
                available_column.remove(value)


        #Positions Related by 3x3 grid constraint
        grid_row_start = (row//3) * 3
        grid_row_end = grid_row_start + 3
        grid_col_start = (column//3) * 3
        grid_col_end = grid_col_start + 3

        for row_2 in range(grid_row_start, grid_row_end):
            for col_2 in range(grid_col_start, grid_col_end):
                value = self.get_idx(row_2, col_2)
                if value != self.empty_slot:
                    available_grid.remove(value)

        set_row = set(available_row)
        set_col = set(available_column)
        set_grid = set(available_grid)
        available_all = list(set_row.intersection(set_col, set_grid))

        return available_row, available_column, available_grid, available_all
    



class BoardLogic:

    @staticmethod
    def check_game_end(state: str) -> bool: #Check if game end is reached (no empty slots)
        return state.count(Board.empty_slot) == 0

    @staticmethod
    def is_valid_idx(i: int, j: int) -> bool:  # Checks if an index is valid
        return 0 <= i < Board.rows and 0 <= j < Board.columns

    @staticmethod    
    def get_idx(state: str, i: int, j: int): # Returns the value at position i,j in the board
        return state[i*Board.columns+j]

    @staticmethod # Sets the value at position i,j in the board
    def set_idx(state: str, i: int, j: int, value: int) -> str:
        state = state[:i*Board.columns+j] + str(value) + state[i*Board.columns+j+1:]
        return state
        
    @staticmethod
    def get_related_positions(row: int, col:int): #Returns a list of positions that cannot have same value as the given position
        related_positions = []

        #Positions Related by row constraint
        for row_2 in range(Board.rows):
            if row_2 != row:
                related_positions.append((row_2, col))
        
        #Positions Related by column constraint
        for col_2 in range(Board.columns):
            if col_2 != col:
               related_positions.append((row, col_2))

        #Positions Related by 3x3 grid constraint
        grid_row_start = (row//3) * 3
        grid_row_end = grid_row_start + 3
        grid_col_start = (col//3) * 3
        grid_col_end = grid_col_start + 3

        for row_2 in range(grid_row_start, grid_row_end):
            for col_2 in range(grid_col_start, grid_col_end):
                if row_2 == row and col_2==col:
                    continue
                elif (row_2, col_2) in related_positions:
                    continue
                else:
                    related_positions.append((row_2, col_2))

        return related_positions


    
    @staticmethod
    def check_valid_move(state: str, i: int, j: int, value: int) -> bool:
        value = str(value)

        #Check Row Constraint
        for k in range(0, Board.columns):
            if BoardLogic.get_idx(state, i, k) == value:
                print("Row Constraint")
                return False
            
        #Check Column Constraint
        for k in range(0, Board.rows):
            if BoardLogic.get_idx(state, k, j) == value:
                print("Column Constraint")
                return False
            
        #3x3 grid constraint
        grid_row_start = (i//3) * 3
        grid_row_end = grid_row_start + 3
        grid_col_start = (j//3) * 3
        grid_col_end = grid_col_start + 3

        for i_grid in range(grid_row_start, grid_row_end):
            for j_grid in range(grid_col_start, grid_col_end):
                if BoardLogic.get_idx(state, i_grid, j_grid) == value:
                    print("Grid Constraint")
                    return False
                
            
        return True
        


    @staticmethod
    def display_board(state: str):
        for i in range(Board.rows):
            print(state[Board.columns*i:Board.columns*(i+1)])

    @staticmethod
    def display_board2(state: str):
        for i in range(Board.rows):
            row = state[Board.columns * i: Board.columns * (i + 1)]
            row_groups = [row[j * 3: (j + 1) * 3] for j in range(3)]
            print(" | ".join(row_groups))
            if (i + 1) % 3 == 0 and i < Board.rows - 1:
                print("-" * 15)  # Print horizontal separator  





