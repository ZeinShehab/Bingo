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
N_BLOCKS = 6

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


def hover(rect):
	if rect.collidepoint(pygame.mouse.get_pos()):
		return True
	return False


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


def play_sound(sound, volume=1):
	pygame.mixer.music.load(sound)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play()

def main():
	global PLAY_HOVER

	grid = np.arange(1, 37)
	np.random.shuffle(grid)
	grid = np.reshape(grid, (6, 6))

	grid2 = np.zeros((6,6))

	win = False
	m_menu = False

	word = "BINGO"
	run = True
	clock = pygame.time.Clock()

	clicked_x = []
	clicked_y = []
	diag_pos = [[0,5], [1,4], [2,3], [3,2], [4,1], [5,0]]
	done_y = []
	done_x = []
	diag = []
	diag2 = []
	n_letters = 0


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
		for column in range(N_BLOCKS):
			for row in range(N_BLOCKS):
				x = (MARGIN + BLOCK_SIZE) * column + MARGIN
				y = (MARGIN + BLOCK_SIZE) * row + MARGIN

				rect = (x, y, BLOCK_SIZE, BLOCK_SIZE)

				if grid2[row,column] == 1:
					WIN.blit(DARK_CIRCLE, (x,y))


				n_diag = 0
				n_diag2 = 0
				if len(diag) == 6:
					n_diag = 1
				elif len(diag) == 12:
					n_diag = 2

				if len(diag2) == 6:
					n_diag2 = 1
				elif len(diag2) == 12:
					n_diag = 2


				text = font.render(str(grid[row, column]), 1, NUM_CLR)
				text_rect = text.get_rect()
				text_rect.x = x+(BLOCK_SIZE/2) - text_rect.width/2
				text_rect.y = y+(BLOCK_SIZE/2) - text_rect.height/2

				if hover(text_rect):
					text = font2.render(str(grid[row, column]), 1, NUM_CLR)

				WIN.blit(text, (x+(BLOCK_SIZE/2) - text_rect.width/2, y+(BLOCK_SIZE/2) - text_rect.height/2))


		# SHOWING BINGO LETTERS
		n = n_letters
		n_letters = len(done_x) + len(done_y) + n_diag + n_diag2

		if n_letters > 0:
			bingo = win_font.render(str(word[0:n_letters]), 1, BINGO_CLR)
			bingo_rect = bingo.get_rect()
			WIN.blit(bingo, ((WIDTH)/2-(bingo_rect.width/2 + (45/2)), HEIGHT-(bingo_rect.height)))

		if n != n_letters:
			play_sound(GET_LETTER, 0.15)


		# SHOWING EXIT BUTTON
		exit_text = exit_font.render("X", 1, (155,0,0))
		exit_rect = exit_text.get_rect()
		exit_rect.x = WIDTH - (exit_rect.width + MARGIN)
		exit_rect.y = HEIGHT - exit_rect.height

		if hover(exit_rect):
			exit_text = exit_font2.render("X", 1, (155,0,0))

		WIN.blit(exit_text, (exit_rect.x, exit_rect.y))


		# WINNING
		if n_letters == 5:
			win = True	

		for i in clicked_y:
			if clicked_y.count(i) >= 6 and i not in done_y:
				done_y.append(i)

		for j in clicked_x:
			if clicked_x.count(j) >= 6 and j not in done_x:
				done_x.append(j)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN and not win:

				pos = pygame.mouse.get_pos()
				column = pos[0] // (BLOCK_SIZE + MARGIN)
				row = pos[1] // (BLOCK_SIZE + MARGIN)

				if row < 6 and column < 6:
					if grid2[row,column] == 1:
						grid2[row,column] = 0

						play_sound(CLICK)

						del clicked_y[clicked_y.index(row)]
						del clicked_x[clicked_x.index(column)]

						try:
							del done_y[done_y.index(row)] 
						except Exception as e:
							pass

						try:
							del done_x[done_x.index(column)]
						except Exception as e:
							pass

						try:
							del diag[diag.index([row,column])]
						except Exception as e:
							pass

						try:
							del diag2[diag2.index([row,column])]
						except Exception as e:
							pass

					else:
						grid2[row,column] = 1

						play_sound(CLICK)

						if row == column:
							diag.append([row,column])
							clicked_y.append(row)
							clicked_x.append(column)

						elif [row,column] in diag_pos:
							diag2.append([row,column])
							clicked_y.append(row)
							clicked_x.append(column)

						else:
							clicked_y.append(row)
							clicked_x.append(column)


				if hover(exit_rect):
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