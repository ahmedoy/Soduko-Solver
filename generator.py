from board import Board
import solver
import random

class BoardGenerator:

    @staticmethod
    def generate_full_board(unique=False, amount_removed=30): #Use unique if the generated board must have 1 unique solution
        generated_board = Board()
        for i in range(3): #First Fill the 3 (3x3) grids on the diagonal
            grid_row_start = (3*i//3) * 3
            grid_row_end = grid_row_start + 3
            grid_col_start = (3*i//3) * 3
            grid_col_end = grid_col_start + 3
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(values)
            for i_grid in range(grid_row_start, grid_row_end):
                for j_grid in range(grid_col_start, grid_col_end):
                    generated_board.set_idx(i_grid, j_grid, values.pop())                    
                    

        #Fill all the other empty slots using arc consistency and backracking
        vars = solver.Variables(generated_board)
        solver.AC_3.AC_3(vars, display=False)
        generated_board.state = solver.Backtracking.Backtracking_Search(vars)

        
        #randomly make some of the filled slots empty again
        board_positions = [i for i in range(81)]
        random.shuffle(board_positions)

        if unique == False:
            for i in range(amount_removed):
                board_position = board_positions.pop()
                generated_board.set_idx(board_position//9, board_position%9, 0)
            return generated_board

        
        #Generate Unique Solution
        amount_removed = min(60, amount_removed) #Prevent more than 60 empty
        removed_count = 0        
        while (removed_count < amount_removed) and (len(board_positions) > 0):
            board_position = board_positions.pop()
            prev_val = generated_board.get_idx(board_position//9, board_position%9)
            generated_board.set_idx(board_position//9, board_position%9, 0)

            #Test if unique
            vars = solver.Variables(generated_board)
            solver.AC_3.AC_3(vars, display=False)
            if solver.Backtracking.Backtracking_Search_CountSolutions(vars) == 1:
                removed_count += 1
            else:
                #Put the value back again
                generated_board.set_idx(board_position//9, board_position%9, prev_val)



        return generated_board



if __name__ == "__main__":
    new_board = BoardGenerator.generate_full_board(unique=False, amount_removed=30)
    new_board.display()
    print("After Solving")
    vars = solver.Variables(new_board)
    solver.AC_3.AC_3(vars)
    new_board.state = solver.Backtracking.Backtracking_Search(vars)
    new_board.display()