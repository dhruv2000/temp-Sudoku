import pygame

class Cell:
    rows = 9
    cols = 9

    '''
    Constructor for the cell class
    For this project, width and height are always 9
    '''
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0

    '''
    Setter for the value displayed in this cell
    '''
    def set(self, val) -> None:
        self.value = val

    '''
    Setter for the temporary value stored in this cell
    (this is the sketched value)
    '''
    def set_temp(self, val) -> None:
        self.temp = val
    
    '''
    win is a pygame window
    This function draws this cell on the pygame window
    '''
    def draw(self, win) -> None:
        fnt = pygame.font.SysFont('comicsans', 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # draw the text in each cell
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5,y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y,gap,gap), 3)

    '''
    solve the sudoku using recursion. visualize the changes in each cell
    '''
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255,255,255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0,0,0))
        win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255,0,0), (x,y,gap,gap), 3)