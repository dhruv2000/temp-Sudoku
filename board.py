import pygame
from cell import Cell
from sudoku_generator import generate_sudoku
from typing import List, Tuple

class Board:
    
    '''
    Parameters:
    for this project: rows, cols, width, and height are 9
    win is a pygame window
    diff indicates the difficulty (easy/medium/hard)

    Sets up a model of the board and its solution
    Both should be stored as 2D Python lists (i.e. List[list])

    Difficulty level -> number of cells to clear:
    easy    ->  30
    medium  ->  40
    hard    ->  50
    '''
    def __init__(self, rows, cols, width, height, win, diff):
        if diff == "easy":
            self.model = generate_sudoku(9, 9)
        elif diff == "medium":
            self.model = generate_sudoku(9, 40)
        else:
            self.model = generate_sudoku(9, 50)

        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win
        self.cells = [[Cell(self.model[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.selected = None
        # v4 set up the copy of original board
        self.original_board = self.model.copy()

    '''
    Draws an outline of the Sudoku board, with bold lines to delineate the 3x3 boxes.
	Draws every Cell in this Board.
    '''
    def draw(self) -> None:
        # draw lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i*gap, 0),
                             (i*gap, self.height), thick)

        # draw cell and text in cells
        # v2
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.win)

    '''
    Marks the cell at (row, col) in the board as the current selected cell.
    Ensures no other cell is selected (only one can be selected at a time)
    '''
    def select(self, row, col):
        # reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    '''
    Given a pos of x,y coordinate and return the row,col number in the board
    If the position is outside the board, return None
    '''
    def click(self, pos) -> Tuple[int, int]:
        # pos: (x, y) coordinate
        # return (row, col)
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            row = int(pos[1] // gap)
            col = int(pos[0] // gap)
            return (row, col)
        else:
            return None

    '''
    Update the temporary/sketched value of the selected cell
    '''
    def sketch(self, key):
        row, col = self.selected
        self.cells[row][col].set_temp(key)

    '''
    If the selected cell was not initially filled in:
    Delete its value and sketched value
    '''
    def clear(self):
        row, col = self.selected
        # v4 if the original board value is 0, then we could remove the digits
        if self.original_board[row][col] == 0:
            self.cells[row][col].set_temp(0)
            self.cells[row][col].set(0)

    '''
    Reset all cells to their original values when the board was generated
    '''
    def reset_to_original(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.model[i][j] = self.original_board[i][j]

        self.cells = [[Cell(self.model[i][j], i, j, self.width, self.height)
                       for j in range(self.cols)] for i in range(self.rows)]

    '''
    If we are able:
    Update the current selected cell so that its filled value is its sketched value
    Return True/False to communicate if the placed value was correct/incorrect

    Called when the user presses the return key
    '''
    def place(self, val) -> bool:
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set(val)
            self.update_model()
            # v3 to see whether entered digit is valid or not
            # if not self.valid(self.model, val, (row,col)):
            #     print("Invalid")
            #     self.cells[row][col].set_temp(0)
            #     self.cells[row][col].set(0)

            if self.valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cells[row][col].set(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    '''
    Test whether the game has been completed
    i.e. the board is completely filled
    '''
    def is_finished(self) -> bool:
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    '''
    keep updating the model(board) with the new values in all cells
    '''
    def update_model(self):
        self.model = [[self.cells[i][j].value for j in range(self.cols)]
            for i in range(self.rows)]

    '''
    check whether the current digit entered is a valid one
    should only called by solve and solve_gui
    '''
    def valid(self, bo, num, pos):
        # check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # check box
        box_x = pos[0] // 3
        box_y = pos[1] // 3

        for i in range(box_x * 3, box_x * 3 + 3):
            for j in range(box_y * 3, box_y * 3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False
        return True

    '''
    find an empty cell (a cell which still needs to be filled in)
    '''
    def find_empty(self):
        for i in range(len(self.model)):
            for j in range(len(self.model[0])):
                if self.model[i][j] == 0:
                    return (i, j)
        return None

    '''
    solve the sudoku recursively
    '''
    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True
                self.model[row][col] = 0
        return False

    '''
    solve the sudoku visually
    This should be called when the user presses the space key
    '''
    def solve_gui(self):
        self.update_model()
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cells[row][col].set(i)
                self.cells[row][col].draw_change(self.win, True)
                # self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cells[row][col].set(0)
                # self.update_model()
                self.cells[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False