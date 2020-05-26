import numpy as np
import pygame
import random
import time
import os
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()


# GLOBAL CONSTANTS
BLOCK_SIZE = 60
MARGIN = 8
N_BLOCKS = 6
NUM_CLR = (0,0,0)
BINGO_CLR = (155,0,0)
WIN_CLR = (155,0,0)

WIDTH = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN
HEIGHT = (BLOCK_SIZE * N_BLOCKS) + (MARGIN * N_BLOCKS) + MARGIN + 75 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("BINGO!")


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


PLAY_HOVER = True

font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 35)
font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 35)
win_font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 70)
win_font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 70)
exit_font = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Light.ttf"), 70)
exit_font2 = pygame.font.Font(os.path.join("assets/Montserrat", "Montserrat-Medium.ttf"), 70)


play_sound = True
menu = True

play_music = True


def main_menu():
	global PLAY_HOVER, menu

	WIN.blit(BG, (0,0))

	play_text = win_font.render("PLAY", 1, NUM_CLR)
	play_rect = play_text.get_rect()
	play_rect.x = WIDTH/2 - play_rect.width/2
	play_rect.y = HEIGHT/2 - play_rect.height/2

	pos = pygame.mouse.get_pos()
	if play_rect.collidepoint(pos):
		if PLAY_HOVER:
			pygame.mixer.music.load(HOVER)
			pygame.mixer.music.set_volume(1)
			pygame.mixer.music.play()
			PLAY_HOVER = False
		play_text = win_font2.render("PLAY", 1, NUM_CLR)
	else:
		PLAY_HOVER = True

	WIN.blit(play_text, (play_rect.x, play_rect.y))

	pygame.display.flip()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if play_rect.collidepoint(event.pos):
				pygame.mixer.music.load(MENU_CLICK)
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
				time.sleep(0.5)
				menu = False
				main()


def end_screen(win):
	global PLAY_HOVER, play_sound

	if win == 0:
		end_text = "YOU WIN!"
		sound = WIN_GAME
	if win == 1:
		end_text = "YOU LOSE!"
		sound = LOSE_GAME

	WIN.blit(BG, (0,0))

	if play_sound:
		pygame.mixer.music.load(sound)
		pygame.mixer.music.play()
		play_sound = False

	win_text = win_font.render(end_text, 1, WIN_CLR)
	win_rect = win_text.get_rect()
	WIN.blit(win_text, (WIDTH/2 - win_rect.width/2, (HEIGHT-75)/2 - win_rect.height/2))

	rest_text = win_font.render("RESTART", 1, NUM_CLR)
	rest_rect = rest_text.get_rect()
	rest_rect.x = WIDTH/2 - rest_rect.width/2
	rest_rect.y = (HEIGHT-75)/2 + win_rect.height+10

	pos = pygame.mouse.get_pos()
	if rest_rect.collidepoint(pos):
		if PLAY_HOVER:
			pygame.mixer.music.load(HOVER)
			pygame.mixer.music.set_volume(1)
			pygame.mixer.music.play()
			PLAY_HOVER = False
		rest_text = win_font2.render("RESTART", 1, NUM_CLR)
	else:
		PLAY_HOVER = True

	WIN.blit(rest_text, (WIDTH/2 - rest_rect.width/2, (HEIGHT-75)/2 + win_rect.height+10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:

			if rest_rect.collidepoint(event.pos):
				pygame.mixer.music.load(MENU_CLICK)
				pygame.mixer.music.set_volume(1)
				pygame.mixer.music.play()
				time.sleep(0.5)
				run = False
				win = False
				lose = False
				main()

	pygame.display.flip()


def main():
	global PLAY_HOVER

	grid = np.arange(1, 37)
	np.random.shuffle(grid)
	grid = np.reshape(grid, (6, 6))

	grid2 = np.zeros((6,6), dtype=int)

	win = False
	lose = False
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

	random_numbers = list(range(1, 37))

	# num_text = win_font.render('', 1, (0,0,0))

	while run:
		if win:
			time.sleep(1)
			while win:
				end_screen(0)
		if lose:
			time.sleep(0.5)
			while lose:
				end_screen(1)

		if m_menu:
			time.sleep(0.5)
			run = False
			win, lose = False, False

			while m_menu:
				main_menu()


		WIN.blit(BG, (0,0))

		for column in range(N_BLOCKS):
			for row in range(N_BLOCKS):
				x = (MARGIN + BLOCK_SIZE) * column + MARGIN
				y = (MARGIN + BLOCK_SIZE) * row + MARGIN

				rect = (x, y, BLOCK_SIZE, BLOCK_SIZE)

				# img = BLUE_CIRCLE
				if grid2[row,column] == 1:
					img = DARK_CIRCLE
					WIN.blit(img, (x,y))


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

				pos = pygame.mouse.get_pos()
				if text_rect.collidepoint(pos):
					text = font2.render(str(grid[row, column]), 1, NUM_CLR)

				WIN.blit(text, (x+(BLOCK_SIZE/2) - text_rect.width/2, y+(BLOCK_SIZE/2) - text_rect.height/2))

		n = n_letters
		n_letters = len(done_x) + len(done_y) + n_diag + n_diag2

		if n_letters > 0:
			bingo = win_font.render(str(word[0:n_letters]), 1, BINGO_CLR)
			bingo_rect = bingo.get_rect()
			WIN.blit(bingo, ((WIDTH)/2-(bingo_rect.width/2 + (45/2)), HEIGHT-(bingo_rect.height)))
		if n_letters == 5:
			win = True	

		if n != n_letters:
			pygame.mixer.music.load(GET_LETTER)
			pygame.mixer.music.set_volume(0.15)
			# pygame.mixer.music.play()

		for i in clicked_y:
			if clicked_y.count(i) >= 6 and i not in done_y:
				done_y.append(i)

		for j in clicked_x:
			if clicked_x.count(j) >= 6 and j not in done_x:
				done_x.append(j)

		# get_num_text = win_font.render("NUM", 1, (0,0,0))
		# get_num_rect = get_num_text.get_rect()
		# get_num_rect.x = WIDTH - (get_num_rect.width+MARGIN)
		# get_num_rect.y = HEIGHT/2 - get_num_rect.height/2

		# num_text_rect = num_text.get_rect()
		# num_text_rect.x = WIDTH - (get_num_rect.width/2 + num_text_rect.width/2 + MARGIN)
		# num_text_rect.y = HEIGHT/2 - (num_text_rect.height/2 + get_num_rect.height)

		exit_text = exit_font.render("X", 1, (155,0,0))
		exit_rect = exit_text.get_rect()
		exit_rect.x = WIDTH - (exit_rect.width + MARGIN)
		exit_rect.y = HEIGHT - exit_rect.height

		if exit_rect.collidepoint(pygame.mouse.get_pos()):
			exit_text = exit_font2.render("X", 1, (155,0,0))

		WIN.blit(exit_text, (exit_rect.x, exit_rect.y))

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

						pygame.mixer.music.load(CLICK)
						pygame.mixer.music.set_volume(1)
						pygame.mixer.music.play()

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

						pygame.mixer.music.load(CLICK)
						pygame.mixer.music.set_volume(1)
						pygame.mixer.music.play()

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


				# if get_num_rect.collidepoint(event.pos):
				# 	pygame.mixer.music.load(CLICK2)
				# 	pygame.mixer.music.set_volume(1)
				# 	pygame.mixer.music.play()

				# 	if len(random_numbers) == 0:
				# 		lose = True
				# 	if not lose:
				# 		num = random.choice(random_numbers)
				# 		del random_numbers[random_numbers.index(num)]

				# 		num_text = win_font.render(str(num),1,WIN_CLR)

				# 		get_num_text = win_font.render("NUM", 1, (0,0,0))

				if exit_rect.collidepoint(event.pos):
					pygame.mixer.music.load(EXIT)
					pygame.mixer.music.play()

					m_menu = True
				else:
					m_menu = False

		ps = pygame.mouse.get_pos()

		# if get_num_rect.collidepoint(ps):
		# 	get_num_text = win_font2.render("NUM", 1, (0,0,0))

		# WIN.blit(num_text, (num_text_rect.x, num_text_rect.y))
		# WIN.blit(get_num_text, (get_num_rect.x, get_num_rect.y))
				
		clock.tick(60)
		pygame.display.flip()


while menu:
	main_menu()