import board
import solver

test_board = board.Board()

initial_state = ["700009050",
                 "040050700",
                 "003000010",
                 "208160000",
                 "000308000",
                 "000027108",
                 "080000500",
                 "009010030",
                 "060200004"]

#Initialize Board with state
test_board.state = "".join(initial_state)

#Create Variables Data Structure (used for AC and Backtracking)
vars = solver.Variables(test_board)

solver.AC_3.AC_3(vars) #Reduce Domains with AC algorithm
print("Domains after reduction with AC")
vars.print_vars() #Print Domains after reduction with AC


test_board.state = solver.Backtracking.Backtracking_Search(vars) #Solve using Backtracking

print("Domains after solution")

vars.print_vars() #Print Domains after solution

print("Board State after solution")

test_board.display() #Print Board State after solution