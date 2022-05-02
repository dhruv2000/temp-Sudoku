import math,random
from typing import List, Tuple

class SudokuGenerator:
    '''
    create a sudoku board - initialize class variables and set up the 2D board
    row_length will always be 9 for this project (the number of rows/columns of the board)
    removed cells will be an integer value - the number of cells to be removed
    '''
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.srn = int(math.sqrt(self.row_length))
        self.board = [[0 for i in range(row_length)] for j in range(row_length)]

    '''
    Returns a 2D python list of numbers which represents the board
    '''
    def get_board(self) -> List[list]:
        return self.board

    '''
    Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes
    '''
    def print_board(self) -> None:
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]), end=" ")

    '''
    Determines if num is contained in the specified row (horizontal) of the board
    '''
    def unusedinrow(self, row, num) -> bool:
        for col in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
    Determines if num is contained in the specified column (vertical) of the board
    '''
    def unusedincol(self, col, num) -> bool:
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    '''
    Determines if num is contained in the 3x3 box specified on the board
    The 3x3 box is from (row_start, col_start) to (row_start+2, col_start+2)
    '''
    def unusedinbox(self, row_start, col_start, num) -> bool:
        for i in range(self.srn):
            for j in range(self.srn):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True
    '''
    Determines if it is safe to enter num at coordinates (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box
    '''
    def check_if_safe(self, row, col, num) -> bool:
        return self.unusedinrow(row, num) and self.unusedincol(col, num) and self.unusedinbox(row - row % self.srn, col - col % self.srn, num)

    '''
    Fills the 3x3 box from (row_start, col_start) to (row_start+2, col_start+2)
    For each position, generates a random digit which has not been used in the box
    '''
    def fill_box(self, row_start, col_start) -> None:
        num = self.random_generator(self.row_length)
        for i in range(self.srn):
            for j in range(self.srn):
                while not self.unusedinbox(row_start, col_start, num):
                    num = self.random_generator(self.row_length)
                self.board[row_start + i][col_start + j] = num

    '''
    Could also use random.randrange(1, num+1) or random.randint(1,num)
    '''
    def random_generator(self, num) -> int:
        res = int(math.floor(random.random() * num + 1))
        return res
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)
    '''
    def fill_diagonal(self) -> None:
        for i in range(0, self.row_length, self.srn):
            self.fill_box(i, i)

    '''
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
    '''
    def fill_remaining(self, row, col) -> bool:
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.srn:
            if col < self.srn:
                col = self.srn
        elif row < self.row_length - self.srn:
            if col == int(row // self.srn * self.srn):
                col += self.srn
        else:
            if col == self.row_length - self.srn:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.check_if_safe(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    TODO: Should this be provided for students?
    Constructs a solution by calling fill_diagonal and fill_remaining
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.srn)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    '''
    def remove_cells(self):
        count = self.removed_cells
        while count != 0:
            cell_num = random.randint(0, self.row_length * self.row_length - 1)
            row = cell_num // self.row_length
            col = cell_num % self.row_length
            if self.board[row][col] != 0:
                count -= 1
                self.board[row][col] = 0

'''
TODO: Should we include this in the template?

Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution
'''
def generate_sudoku(size, removed) -> Tuple[List[list], List[list]]:
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

# def main():
#     board = generate_sudoku()
#     for i in range(len(board)):
#         for j in range(len(board[0])):
#             if j == 8:
#                 print(board[i][j])
#             else:
#                 print(str(board[i][j]) + " ", end="")



# main()