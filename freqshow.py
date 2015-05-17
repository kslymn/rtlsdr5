import os
import time

import pygame

import controller
import model
import ui



SDR_SAMPLE_SIZE = 1024	# 3.5 LCD Ekran icin en uygun boyut.

CLICK_DEBOUNCE  = 0.4	# Dokunma tepki suresi.


MAIN_FONT = 33
NUM_FONT  = 50


MAIN_BG        = (  0,   0,   0) # Black
INPUT_BG       = ( 60, 255, 255) # Cyan-ish
INPUT_FG       = (  0,   0,   0) # Black
CANCEL_BG      = (128,  45,  45) # Dark red
ACCEPT_BG      = ( 45, 128,  45) # Dark green
BUTTON_BG      = ( 60,  60,  60) # Dark gray
BUTTON_FG      = (255, 255, 255) # White
BUTTON_BORDER  = (200, 200, 200) # White/light gray
INSTANT_LINE   = (  0, 255, 128) # Bright yellow green.




ui.MAIN_FONT = MAIN_FONT
ui.Button.fg_color     = BUTTON_FG
ui.Button.bg_color     = BUTTON_BG
ui.Button.border_color = BUTTON_BORDER
ui.Button.padding_px   = 2
ui.Button.border_px    = 2


if __name__ == '__main__':

	pygame.display.init()
	pygame.font.init()
	pygame.mouse.set_visible(True)
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	# Baslangic Ekrani.
	splash = pygame.image.load('spectrum_analyzer.png')
	screen.fill(MAIN_BG)
	screen.blit(splash, ui.align(splash.get_rect(), (0, 0, size[0], size[1])))
	pygame.display.update()
	splash_start = time.time()

	
	fsmodel = model.FreqShowModel(size[0], size[1])
	fscontroller = controller.FreqShowController(fsmodel)
	time.sleep(2.0)
	lastclick = 0
	while True:
		
		for event in pygame.event.get():
			if event.type is pygame.MOUSEBUTTONDOWN \
				and (time.time() - lastclick) >= CLICK_DEBOUNCE:
				lastclick = time.time()
				fscontroller.current().click(pygame.mouse.get_pos())
		
		fscontroller.current().render(screen)
		pygame.display.update()
