import numpy as np
import pygame
import random
import time
import os
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.display.set_caption("BINGO!")


# GLOBAL CONSTANTS
BLOCK_SIZE = 60
MARGIN = 8
N_BLOCKS = 6		# SIZE OF GRID SQUARE
RANGE = 36			# RANGE OF NUMBERS

if RANGE < N_BLOCKS*N_BLOCKS:
	RANGE = N_BLOCKS*N_BLOCKS

# COLORS
NUM_CLR = (0,0,0)
BINGO_CLR = (155,0,0)
WIN_CLR = (155,0,0)

# GAME WINDOW 
WIDTH = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN
HEIGHT = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN + 75 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# LOADING IMAGES
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.jpg")), (WIDTH, HEIGHT))
CIRCLE = pygame.image.load(os.path.join("assets", "dark_circle.png"))
DARK_CIRCLE = pygame.transform.scale(CIRCLE, (BLOCK_SIZE, BLOCK_SIZE))

# LOADING AUDIO
HOVER = os.path.join("assets", "hover.mp3")
CLICK = os.path.join("assets", "click.mp3")
CLICK2 = os.path.join("assets", "click2.mp3")
MENU_CLICK = os.path.join("assets", "menu_click.mp3")
GET_LETTER = os.path.join("assets", "letter.mp3")
WIN_GAME = os.path.join("assets", "positive.wav")
LOSE_GAME = os.path.join("assets", "negative.wav")
EXIT = os.path.join("assets", "exit.mp3")

# FONTS
font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 35)
font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 35)
win_font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 70)
win_font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 70)
exit_font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 70)
exit_font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 70)


PLAY_HOVER = True
PLAY = True
play_music = True


def main_menu():
	global PLAY_HOVER, PLAY


	WIN.blit(BG, (0,0))


	# PLAY TEXT
	play_text = win_font.render("PLAY", 1, NUM_CLR)
	play_rect = play_text.get_rect()
	play_rect.x = WIDTH/2 - play_rect.width/2
	play_rect.y = HEIGHT/2 - play_rect.height/2

	if hover(play_rect):
		if PLAY_HOVER:
			play_sound(HOVER)
			PLAY_HOVER = False
		play_text = win_font2.render("PLAY", 1, NUM_CLR)
	else:
		PLAY_HOVER = True


	WIN.blit(play_text, (play_rect.x, play_rect.y))

	pygame.display.flip()


	# CLICK ON PLAY
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if hover(play_rect):
				play_sound(MENU_CLICK)
				time.sleep(0.5)
				menu = False
				main()


def end_screen():
	global PLAY_HOVER, PLAY


	if PLAY:
		play_sound(WIN_GAME)
		PLAY = False

	# DISPLAYING TEXT
	win_text = win_font.render("YOU WIN!", 1, WIN_CLR)
	win_rect = win_text.get_rect()

	rest_text = win_font.render("RESTART", 1, NUM_CLR)
	rest_rect = rest_text.get_rect()
	rest_rect.x = WIDTH/2 - rest_rect.width/2
	rest_rect.y = (HEIGHT-75)/2 + win_rect.height+10


	# MAKING TEXT INTERACTIVE
	if hover(rest_rect):
		if PLAY_HOVER:
			play_sound(HOVER)
			PLAY_HOVER = False
		rest_text = win_font2.render("RESTART", 1, NUM_CLR)
	else:
		PLAY_HOVER = True


	WIN.blit(BG, (0,0))
	WIN.blit(win_text, (WIDTH/2 - win_rect.width/2, (HEIGHT-75)/2 - win_rect.height/2))
	WIN.blit(rest_text, (WIDTH/2 - rest_rect.width/2, (HEIGHT-75)/2 + win_rect.height+10))


	# CLICK ON RESTART
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if hover(rest_rect):
				play_sound(MENU_CLICK)

				time.sleep(0.5)
				run = False
				win = False
				lose = False
				main()


	pygame.display.flip()


def hover(rect):
	if rect.collidepoint(pygame.mouse.get_pos()):
		return True
	return False


def play_sound(sound, volume=1):
	pygame.mixer.music.load(sound)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play()


def show_numbers(grid1, grid2):
	for column in range(N_BLOCKS):
		for row in range(N_BLOCKS):
			x = (MARGIN + BLOCK_SIZE) * column + MARGIN
			y = (MARGIN + BLOCK_SIZE) * row + MARGIN

			rect = (x, y, BLOCK_SIZE, BLOCK_SIZE)

			if grid2[row,column] == 1:
				WIN.blit(DARK_CIRCLE, (x,y))


			text = font.render(str(grid1[row, column]), 1, NUM_CLR)
			text_rect = text.get_rect()
			text_rect.x = x+(BLOCK_SIZE/2) - text_rect.width/2
			text_rect.y = y+(BLOCK_SIZE/2) - text_rect.height/2

			if hover(text_rect):
				text = font2.render(str(grid1[row, column]), 1, NUM_CLR)

			WIN.blit(text, (x+(BLOCK_SIZE/2) - text_rect.width/2, y+(BLOCK_SIZE/2) - text_rect.height/2))


def show_letters(n1, n2):
	word = "BINGO"

	if n2 > 0:
		bingo = win_font.render(str(word[0:n2]), 1, BINGO_CLR)
		bingo_rect = bingo.get_rect()
		WIN.blit(bingo, ((WIDTH)/2-(bingo_rect.width/2 + (45/2)), HEIGHT-(bingo_rect.height)))

	if n1 != n2:
		play_sound(GET_LETTER, 0.15)


def exit_btn():
	exit_text = exit_font.render("X", 1, (155,0,0))
	exit_rect = exit_text.get_rect()
	exit_rect.x = WIDTH - (exit_rect.width + MARGIN)
	exit_rect.y = HEIGHT - exit_rect.height

	if hover(exit_rect):
		exit_text = exit_font2.render("X", 1, (155,0,0))

	WIN.blit(exit_text, (exit_rect.x, exit_rect.y))

	return exit_rect


def main():
	global PLAY_HOVER


	grid = random.sample(range(1, RANGE+1), N_BLOCKS*N_BLOCKS)
	grid = np.array(grid)
	grid = np.reshape(grid, (N_BLOCKS, N_BLOCKS))

	grid2 = np.zeros((N_BLOCKS,N_BLOCKS))

	run = True
	win = False
	m_menu = False
	clock = pygame.time.Clock()

	diag_pos = [[0,5], [1,4], [2,3], [3,2], [4,1], [5,0]]						# FIX ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	n_letters = 0
	clicked = []
	tkn_pos = []


	# MAIN GAMELOOP
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


		WIN.blit(BG, (0,0))


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
			if clicked.count(i)	>= N_BLOCKS and i not in tkn_pos:
				tkn_pos.append(i)		


		for event in pygame.event.get():
			# QUIT
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			# CLICK
			if event.type == pygame.MOUSEBUTTONDOWN and not win:

				pos = pygame.mouse.get_pos()
				column = pos[0] // (BLOCK_SIZE + MARGIN)
				row = pos[1] // (BLOCK_SIZE + MARGIN)

				commands = [
				lambda: clicked.remove(f"{row}y"),
				lambda: clicked.remove(f"{column}x"),
				lambda: clicked.remove("d1"),
				lambda: clicked.remove("d2"),
				lambda: tkn_pos.remove(f"{row}y"),
				lambda: tkn_pos.remove(f"{column}x"),
				lambda: tkn_pos.remove("d1"),
				lambda: tkn_pos.remove("d2")
				]

				if row < N_BLOCKS and column < N_BLOCKS:
					# IF ALREADY CLICKED: UNCLICK
					if grid2[row,column] == 1:
						grid2[row,column] = 0

						play_sound(CLICK)

						for cmd in commands:
							try:
								cmd()
							except ValueError:
								pass

					# IF NOT CLICKED: CLICK
					else:
						grid2[row,column] = 1

						play_sound(CLICK)

						if row == column:
							clicked.append("d1")

						elif [row,column] in diag_pos:
							clicked.append("d2")

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


menu = True
while menu:
	main_menu()