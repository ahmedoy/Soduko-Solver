from collections import deque
from board import Board, BoardLogic

class Variable:
    def __init__(self, assigned: bool, domain, row:int, col:int):
        self.assigned = assigned #If assigned = true, domain must be a single value
        if self.assigned:
            assert (isinstance(domain, tuple) and len(domain) == 1), "If assigned is True, domain must be a tuple of length 1"

        assert 0 <= row < Board.rows, f"Row should be between 0 and {Board.rows}" #Check if row/col between 0 and 8 (including 8)
        assert 0 <= col < Board.columns, f"Column should be between 0 and {Board.columns}"

        self.domain = domain
        self.row = row
        self.col = col

    def print_variable(self):
        print(f"Row: {self.row}, Column: {self.col}, Domain: {self.domain}")


class Variables:
    def __init__(self, initial_board: Board):
        self.variables_list = [] #Create 2d list of variables
        for i in range(Board.rows):
            for j in range(Board.columns):
                if initial_board.get_idx(i, j) == Board.empty_slot:# if variable is unassigned
                    self.variables_list.append(Variable(assigned=False, domain=list(Board.value_domain), row=i, col=j)) 

                else: #if variable is assigned
                   self.variables_list.append(Variable(assigned=True, domain=(int(initial_board.get_idx(i, j)), ), row=i, col=j))  

    def get_var(self, row, col):
        return self.variables_list[row * Board.columns + col]
    

    def print_vars(self):
        for var in self.variables_list:
            var.print_variable()



        


class Arc:
    def __init__(self, var1: Variable, var2: Variable): #Order matters in Arc consistency (swapping var1 and var2 gives a differenct arc)
        self.var1 = var1
        self.var2 = var2

    def get_arc_id(self): #returns a unique string identifier for the arc 
        return f"{self.var1.row}{self.var1.col}{self.var2.row}{self.var2.col}"
    
    def display_arc(self):
        print(f"Arc Between ({self.var1.row},{self.var1.col}) and ({self.var2.row},{self.var2.col})")        
        
class AC_3:  #Arc Consistency Algorithm

    @staticmethod
    def AC_3(variables: Variables): 
        arc_queue = deque()
        arc_set = set()

        #Create Arcs and add them to the queue
        for row in range(Board.rows):
            for col in range(Board.columns):
                var_1 = variables.get_var(row, col) #Var 1 in Arc
                related_var_positions = BoardLogic.get_related_positions(row, col) #All positions related to var 1 by row/col/grid constraints
                for var_position in related_var_positions:
                    var_2 = variables.get_var(var_position[0], var_position[1])
                    arc = Arc(var_1, var_2)
                    arc_queue.append(arc) 
                    arc_set.add(arc.get_arc_id())

        while len(arc_queue) > 0:
            popped_arc = arc_queue.popleft()
            arc_set.remove(popped_arc.get_arc_id())
            if AC_3.revise(popped_arc):
                if len(popped_arc.var1.domain) == 0:
                    return False #No solution found
                
                else: #Reinsert variables it is related to into the queue (neighbors)
                    related_var_positions = BoardLogic.get_related_positions(popped_arc.var1.row, popped_arc.var1.col)
                    for var_position in related_var_positions:
                        if var_position[0] == popped_arc.var2.row and var_position[1] == popped_arc.var2.col: #Check that Xk isn't equal to Xj (lecture pseudocode)
                            continue
                        else:
                            new_var1 = variables.get_var(var_position[0], var_position[1]) #Xk in pseudocode
                            new_var2 = popped_arc.var1 #Xi in pseudocode
                            new_arc = Arc(new_var1, new_var2)
                            if new_arc.get_arc_id() not in arc_set:
                                arc_queue.append(new_arc)
                                arc_set.add(new_arc.get_arc_id())

        return True
    

    @staticmethod
    def revise(arc: Arc):
        revised = False
        new_var1_domain = []
        for var1_value in arc.var1.domain:
            var1_value_removed = True #flag to check if var1_value will be removed from var1's domain
            for var2_value in arc.var2.domain:
                if var1_value != var2_value: #Keep current value of variable 1 in the domain since there is a value for val 2 that is consistent with it
                    new_var1_domain.append(var1_value) 
                    var1_value_removed = False
                    break #Move to next value of variable 1
            
            
            if var1_value_removed:
                revised = True

        #Update domain of var1
        arc.var1.domain = new_var1_domain
        return revised


