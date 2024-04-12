from collections import deque
from board import Board

class Variable:
    def __init__(self, assigned: bool, domain, row:int, col:int):
        self.assigned = assigned #If assigned = true, domain must be a single value
        if self.assigned:
            assert isinstance(domain, int) or (isinstance(domain, list) and len(domain) == 1), "If assigned is True, domain must be an integer or a list of length 1"

        assert 0 <= row < Board.rows, f"Row should be between 0 and {Board.rows}" #Check if row/col between 0 and 8 (including 8)
        assert 0 <= col < Board.columns, f"Column should be between 0 and {Board.columns}"

        self.domain = domain
        self.row = row
        self.col = col

    def print_variable(self):
        print(f"Row: {self.row}, Column: {self.col}, Domain: {self.domain}")

class Variables:
    def __init__(self, initial_board: Board):
        self.variables_list = [[None for j in range(Board.columns)] for i in range(Board.rows)] #Create 2d list of variables
        for i in range(Board.rows):
            for j in range(Board.columns):
                if initial_board.get_idx(i, j) == Board.empty_slot:# if variable is unassigned
                    self.variables_list[i][j] = Variable(assigned=False, domain=list(Board.value_domain), row=i, col=j)

                else: #if variable is assigned
                   self.variables_list[i][j] = Variable(assigned=True, domain=int(initial_board.get_idx(i, j)), row=i, col=j) 

        


class Arc:
    def __init__(self, var1: Variable, var2: Variable): #Order matters in Arc consistency (swapping var1 and var2 gives a differenct arc)
        self.var1 = var1
        self.var2 = var2
        
        
        