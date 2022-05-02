import pygame
import time
import sys
import button
from board import Board

diff = "easy"
screen = "start"


def showStartScreen(win, easy_button, med_button, hard_button, background_img):
    global diff
    global screen
    fnt = pygame.font.SysFont("comicsans", 75)
    fnt2 = pygame.font.SysFont("comicsans", 60)
    text = fnt.render("Welcome to Sudoku", 1, (0, 0, 0))
    text2 = fnt2.render("Select Game Mode:", 1, (0, 0, 0))

    # win.fill((255, 255, 255))
    # win.fill((202, 228, 241))
    win.blit(background_img, (0, 0))

    win.blit(text, (25, 100))
    win.blit(text2, (70, 275))
    # draw_press_key_message(win)
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        # This is needed to check for a key press and to not brick the game
        key_pressed = check_key_press()
        # Render the buttons and move to next screen if clicked
        if easy_button.draw(win):
            print('EASY')
            diff = "easy"
            pygame.display.update()
            screen = "board"
            return

        if med_button.draw(win):
            print('MEDIUM')
            diff = "medium"
            pygame.display.update()
            screen = "board"
            return

        if hard_button.draw(win):
            print('HARD')
            diff = "hard"
            pygame.display.update()
            screen = "board"
            return

        pygame.display.update()


def showGameWonScreen(win, exit_button_2, background_img):
    global screen
    fnt = pygame.font.SysFont("comicsans", 100)
    text = fnt.render("Game Won!", 1, (0, 0, 0))
    # win.fill((255, 255, 255))
    # win.fill((202, 228, 241))
    win.blit(background_img, (0, 0))
    win.blit(text, (70, 150))
    # draw_press_key_message(win)
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        key_pressed = check_key_press()
        if exit_button_2.draw(win):
            screen = "start"
            print('EXIT')
            pygame.display.update()
            return
        pygame.display.update()


def showGameOverScreen(win, restart_button_2, background_img):
    global screen
    fnt = pygame.font.SysFont("comicsans", 100)
    text = fnt.render("Game Over :(", 1, (0, 0, 0))
    # win.fill((255, 255, 255))
    # win.fill((202, 228, 241))
    win.blit(background_img, (0, 0))
    win.blit(text, (50, 150))
    # draw_press_key_message(win)
    pygame.display.update()
    pygame.time.wait(500)

    while True:
        key_pressed = check_key_press()
        if restart_button_2.draw(win):
            screen = "start"
            print('RESTART')
            pygame.display.update()
            return
        pygame.display.update()


def terminate():
    pygame.quit()
    sys.exit()


def check_key_press():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


# def draw_press_key_message(win):
#     fnt = pygame.font.SysFont("comicsans", 20)
#     text = fnt.render(
#         "Press 'e' for Easy, 'm' for Medium, and 'h' for a Hard Sodoku", 1, (0, 0, 0))
#     win.blit(text, (260-200, 600-50))


def runGame(win, reset_button, exit_button, restart_button_2, restart_button, background_img):
    global screen
    board = Board(9, 9, 540, 540, win, diff)
    run = True
    key = None
    start = time.time()
    strikes = 0
    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            # If the exit button gets pressed
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                # v3, use the left,right,up and down arrow to move the cursor
                if event.key == pygame.K_LEFT:
                    row, col = board.selected
                    if col > 0:
                        col -= 1
                        board.select(row, col)
                elif event.key == pygame.K_RIGHT:
                    row, col = board.selected
                    if col < board.cols - 1:
                        col += 1
                        board.select(row, col)
                elif event.key == pygame.K_UP:
                    row, col = board.selected
                    if row > 0:
                        row -= 1
                        board.select(row, col)
                elif event.key == pygame.K_DOWN:
                    row, col = board.selected
                    if row < board.rows - 1:
                        row += 1
                        board.select(row, col)

                # v4
                # solve the gui interface
                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    return

                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None

                if event.key == pygame.K_RETURN:
                    select = board.selected
                    if select:
                        row, col = select
                        if board.cells[row][col].temp != 0:
                            if board.place(board.cells[row][col].temp):
                                print("Success!")
                            else:
                                print("Wrong")
                                strikes += 1
                            key = None

                            if board.is_finished():
                                screen = "won"
                                print("Game Over! YOU WON!")
                                return
            if reset_button.draw(win):
                print('RESET BOARD 1')
                strikes = 0
                board.reset_to_original()
                pygame.display.update()
            if restart_button.draw(win):
                print('RESTART GAME')
                screen = "start"
                pygame.display.update()
                return

        if board.selected and key:
            board.sketch(key)
            key = None
        # v4, replace with redraw_window method
        # win.fill((255,255,255))
        # board.draw()
        redraw_window(win, board, play_time, strikes,
                      restart_button_2, background_img)
        # If the screen has been reset to start
        if screen == "start":
            return
        if reset_button.draw(win):
            # This actually never gets called but is needed for no bugs
            print("Reset board 2")
            strikes = 0
            board.reset_to_original()
            pygame.display.update()
        restart_button.draw(win)

        if exit_button.draw(win):
            pygame.display.update()
            run = False
            pygame.quit()
            sys.exit()
        pygame.display.update()


# v4
# draw time and board inside of redraw_window function
def redraw_window(win, board, time, strikes, restart_button_2, background_img):
    global screen
    # win.fill((255, 255, 255))
    win.fill((202, 228, 241))

    # draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540-160, 560))
    # draw strikes
    if(strikes < 3):
        text = fnt.render("X " * strikes, 1, (255, 0, 0))
    else:
        # GAME OVER SCREEN - need to show a key to close window or start again
        screen = "end"
        strikes = 0
        showGameOverScreen(win, restart_button_2, background_img)
        return
    win.blit(text, (20, 560))
    # draw grid and board
    board.draw()

# v4
# format the time


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((540, 600))
    # win.fill((202, 228, 241))

    # load button images
    easy_img = pygame.image.load('easy.png').convert_alpha()
    # easy2_img = pygame.image.load('easy2.png').convert_alpha()
    med_img = pygame.image.load('medium.png').convert_alpha()
    hard_img = pygame.image.load('hard.png').convert_alpha()
    exit_img = pygame.image.load('exit.png').convert_alpha()
    restart_img = pygame.image.load('restart.png').convert_alpha()
    reset_img = pygame.image.load('reset.png').convert_alpha()
    # background_img = pygame.image.load('background.jpg').convert_alpha()
    background_img = pygame.image.load('background.jpg')
    background_img = pygame.transform.scale(background_img, (540, 600))

    # create button instances
    easy_button = button.Button(60, 375, easy_img, 0.4)
    # easy2_button = button.Button(60, 375, easy2_img, 0.4)
    med_button = button.Button(200, 375, med_img, 0.4)
    hard_button = button.Button(340, 375, hard_img, 0.4)
    exit_button = button.Button(280, 540, exit_img, 0.7)
    restart_button = button.Button(190, 540, restart_img, 0.7)
    reset_button = button.Button(100, 540, reset_img, 0.3)
    exit_button_2 = button.Button(170, 300, exit_img, 1.2)
    restart_button_2 = button.Button(170, 300, restart_img, 1.2)
    # restart_button_2 = button.Button(170, 300, restart_img, 1.2)

    pygame.display.set_caption('Sudoku')
    showStartScreen(win, easy_button, med_button, hard_button, background_img)
    while screen != "start":
        runGame(win, reset_button, exit_button,
                restart_button_2, restart_button, background_img)
        # This is for when the user clicks 'reset' from the board screen
        if (screen == "start"):
            showStartScreen(win, easy_button, med_button,
                            hard_button, background_img)
        elif (screen == "won"):
            showGameWonScreen(win, exit_button_2, background_img)
        else:
            showGameOverScreen(win, restart_button_2, background_img)


main()
