import numpy as np
import pygame
import random
import time
import os
import sys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.display.set_caption("BINGO!")

# GLOBAL CONSTANTS
BLOCK_SIZE = 60
MARGIN = 10
N_BLOCKS = 6  # SIZE OF GRID SQUARE
RANGE = 36  # RANGE OF NUMBERS

if RANGE < N_BLOCKS * N_BLOCKS:
    RANGE = N_BLOCKS * N_BLOCKS

# GLOBAL VARIABLES
PLAY_HOVER = True
PLAY = True

# COLORS
ACCENT = (130, 30, 30)
NUM_CLR = (0, 0, 0)
MENU_CLR = (0, 0, 0)

# GAME WINDOW 
WIDTH = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN
HEIGHT = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN + 75
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# LOADING IMAGES
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "bg.jpg")), (WIDTH, HEIGHT))
CIRCLE = pygame.transform.scale(pygame.image.load(os.path.join("assets/Images", "circle.png")),
                                (BLOCK_SIZE, BLOCK_SIZE))

# LOADING AUDIO
HOVER = os.path.join("assets/Audio", "hover.mp3")
CLICK = os.path.join("assets/Audio", "click.mp3")
CLICK2 = os.path.join("assets/Audio", "click2.mp3")
MENU_CLICK = os.path.join("assets/Audio", "menu_click.mp3")
GET_LETTER = os.path.join("assets/Audio", "letter.mp3")
WIN_GAME = os.path.join("assets/Audio", "positive.wav")
LOSE_GAME = os.path.join("assets/Audio", "negative.wav")
EXIT = os.path.join("assets/Audio", "exit.mp3")

# LOADING FONTS
NUM_FONT = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 35)
NUM_FONT_2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 35)
MENU_FONT = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 70)
MENU_FONT_2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 70)


def main_menu():
    global PLAY_HOVER, PLAY

    menu = True
    while menu:
        WIN.blit(BG, (0, 0))

        # PLAY TEXT
        play_text = MENU_FONT.render("PLAY", 1, MENU_CLR)
        play_rect = play_text.get_rect()
        play_rect.x = int(WIDTH / 2 - play_rect.width / 2)
        play_rect.y = int(HEIGHT / 2 - play_rect.height / 2)

        if hover(play_rect):
            if PLAY_HOVER:
                play_sound(HOVER)
                PLAY_HOVER = False
            play_text = MENU_FONT_2.render("PLAY", 1, ACCENT)
        else:
            PLAY_HOVER = True

        WIN.blit(play_text, (play_rect.x, play_rect.y))

        pygame.display.flip()

        # CLICK ON PLAY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover(play_rect):
                    play_sound(MENU_CLICK)
                    time.sleep(0.5)
                    main()


def end_screen():
    global PLAY_HOVER, PLAY

    if PLAY:
        play_sound(WIN_GAME)
        PLAY = False

    # DISPLAYING TEXT
    win_text = MENU_FONT.render("YOU WIN!", 1, ACCENT)
    win_rect = win_text.get_rect()
    win_rect.x = int(WIDTH / 2 - win_rect.width / 2)
    win_rect.y = int((HEIGHT - 75) / 2 - win_rect.height / 2)

    rest_text = MENU_FONT.render("RESTART", 1, MENU_CLR)
    rest_rect = rest_text.get_rect()
    rest_rect.x = int(WIDTH / 2 - rest_rect.width / 2)
    rest_rect.y = int((HEIGHT - 75) / 2 + win_rect.height + 10)

    # MAKING RESTART INTERACTIVE
    if hover(rest_rect):
        if PLAY_HOVER:
            play_sound(HOVER)
            PLAY_HOVER = False
        rest_text = MENU_FONT_2.render("RESTART", 1, ACCENT)
    else:
        PLAY_HOVER = True

    WIN.blit(BG, (0, 0))
    WIN.blit(win_text, (win_rect.x, win_rect.y))
    WIN.blit(rest_text, (rest_rect.x, rest_rect.y))

    # CLICK ON RESTART
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if hover(rest_rect):
                play_sound(MENU_CLICK)

                time.sleep(0.5)
                main()

    pygame.display.flip()


def hover(rect):
    if rect.collidepoint(pygame.mouse.get_pos()):
        return True
    return False


def play_sound(sound, volume=1.0):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


def show_numbers(grid1, grid2):
    for column in range(N_BLOCKS):
        for row in range(N_BLOCKS):
            x = (MARGIN + BLOCK_SIZE) * column + MARGIN
            y = (MARGIN + BLOCK_SIZE) * row + MARGIN

            if grid2[row, column] == 1:
                WIN.blit(CIRCLE, (x, y))

            text = NUM_FONT.render(str(grid1[row, column]), 1, NUM_CLR)
            text_rect = text.get_rect()
            text_rect.x = int(x + (BLOCK_SIZE / 2) - text_rect.width / 2)
            text_rect.y = int(y + (BLOCK_SIZE / 2) - text_rect.height / 2)

            if hover(text_rect):
                text = NUM_FONT_2.render(str(grid1[row, column]), 1, ACCENT)

            WIN.blit(text, (text_rect.x, text_rect.y))


def show_letters(n1, n2):
    word = "BINGO"

    if n2 > 0:
        bingo = MENU_FONT.render(str(word[0:n2]), 1, ACCENT)
        bingo_rect = bingo.get_rect()
        bingo_rect.x = int(WIDTH / 2 - (bingo_rect.width / 2 + (45 / 2)))
        bingo_rect.y = int(HEIGHT - bingo_rect.height)

        WIN.blit(bingo, (bingo_rect.x, bingo_rect.y))

    if n1 != n2:
        play_sound(GET_LETTER, 0.15)


def exit_btn():
    exit_text = MENU_FONT.render("x", 1, ACCENT)
    exit_rect = exit_text.get_rect()
    exit_rect.x = int(WIDTH - (exit_rect.width + 2 * MARGIN))
    exit_rect.y = int(HEIGHT - exit_rect.height)

    if hover(exit_rect):
        exit_text = MENU_FONT_2.render("x", 1, ACCENT)

    WIN.blit(exit_text, (exit_rect.x, exit_rect.y))

    return exit_rect


def main():
    global PLAY_HOVER

    grid = random.sample(range(1, RANGE + 1), N_BLOCKS * N_BLOCKS)
    grid = np.array(grid)
    grid = np.reshape(grid, (N_BLOCKS, N_BLOCKS))

    grid2 = np.zeros((N_BLOCKS, N_BLOCKS))

    run = True
    win = False
    m_menu = False
    clock = pygame.time.Clock()

    n_letters = 0
    clicked = []
    tkn_pos = []

    # DIAGONAL
    n1 = 0
    n2 = N_BLOCKS - 1
    diag_pos = []
    for _ in range(0, N_BLOCKS):
        diag_pos.append([n1, n2])
        n1 += 1
        n2 -= 1

    # MAIN GAME LOOP
    while run:
        if win:
            time.sleep(1)
            while win:
                end_screen()

        if m_menu:
            time.sleep(0.5)
            run = False

            while m_menu:
                main_menu()

        WIN.blit(BG, (0, 0))

        # SHOWING NUMBERS
        show_numbers(grid, grid2)

        # SHOWING BINGO LETTERS
        n = n_letters
        n_letters = len(tkn_pos)

        show_letters(n, n_letters)

        # SHOWING EXIT BUTTON
        exit_btn()

        # WINNING
        if n_letters == 5:
            win = True

        # CHECKING IF GOT LETTER
        for i in clicked:
            if clicked.count(i) >= N_BLOCKS and i not in tkn_pos:
                tkn_pos.append(i)

        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # CLICK
            if event.type == pygame.MOUSEBUTTONDOWN and not win:

                pos = pygame.mouse.get_pos()
                column = pos[0] // (BLOCK_SIZE + MARGIN)
                row = pos[1] // (BLOCK_SIZE + MARGIN)

                if row < N_BLOCKS and column < N_BLOCKS:
                    # IF ALREADY CLICKED: UN-CLICK
                    if grid2[row, column] == 1:
                        grid2[row, column] = 0

                        play_sound(CLICK)

                        # REMOVE FROM D1
                        if row == column:
                            clicked.remove("d1")

                            if "d1" in tkn_pos:
                                tkn_pos.remove("d1")

                        # REMOVE FROM D2
                        if [row, column] in diag_pos:
                            clicked.remove("d2")

                            if "d2" in tkn_pos:
                                tkn_pos.remove("d2")

                        # REMOVE X AND Y
                        clicked.remove(f"{row}y")
                        clicked.remove(f"{column}x")

                        if f"{row}y" in tkn_pos:
                            tkn_pos.remove(f"{row}y")

                        if f"{column}x" in tkn_pos:
                            tkn_pos.remove(f"{column}x")

                    # IF NOT CLICKED: CLICK
                    else:
                        grid2[row, column] = 1

                        play_sound(CLICK)

                        # ADD TO D1
                        if row == column:
                            clicked.append("d1")

                        # ADD TO D2
                        elif [row, column] in diag_pos:
                            clicked.append("d2")

                        # ADD X AND Y
                        clicked.append(f"{row}y")
                        clicked.append(f"{column}x")

                if hover(exit_btn()):
                    play_sound(EXIT)

                    m_menu = True
                else:
                    m_menu = False

        # GAME CLOCK
        clock.tick(60)

        pygame.display.flip()


main_menu()
