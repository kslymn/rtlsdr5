import pygame



ALIGN_LEFT   = 0.0
ALIGN_TOP    = 0.0
ALIGN_CENTER = 0.5
ALIGN_RIGHT  = 1.0
ALIGN_BOTTOM = 1.0


def align(child, parent, horizontal=ALIGN_CENTER, vertical=ALIGN_CENTER,
	hpad=0, vpad=0):

	cx, cy, cwidth, cheight = child
	px, py, pwidth, pheight = parent
	return (px+(horizontal*pwidth-horizontal*cwidth)+hpad,
			py+(vertical*pheight-vertical*cheight)+vpad)

font_cache = {}
def get_font(size):
	
	if size not in font_cache:
		font_cache[size] = pygame.font.Font(None, size)
	return font_cache[size]

def render_text(text, size=33, fg=(255, 255, 255), bg=(0, 0, 0)):

	if bg is not None:
	
		return get_font(size).render(text, True, fg, bg)
	else:
		
		return get_font(size).render(text, True, fg)


class Button(object):

	fg_color     = (255, 255, 255)
	bg_color     = (60, 60, 60)
	border_color = (200, 200, 200)
	padding_px   = 2
	border_px    = 2
	font_size    = 33

	def __init__(self, rect, text, click=None, font_size=None, bg_color=None):
		
		self.text = text
		self.bg_color = bg_color if bg_color is not None else self.bg_color
		self.font_size = font_size if font_size is not None else self.font_size
		self.click_func = click
		
		x, y, width, height = rect
		x += self.padding_px
		y += self.padding_px
		width -= 2*self.padding_px
		height -= 2*self.padding_px
		self.rect = (x, y, width, height)
		
		self.label = render_text(text, size=self.font_size, fg=self.fg_color,
			bg=self.bg_color)
		self.label_pos = align(self.label.get_rect(), self.rect)

	def render(self, screen):
	
		screen.fill(self.bg_color, self.rect)
		pygame.draw.rect(screen, self.border_color, self.rect, self.border_px)
		screen.blit(self.label, self.label_pos)

	def click(self, location):
		
		x, y, width, height = self.rect
		mx, my = location
		if mx >= x and mx <= (x + width) and my >= y and my <= (y + height) \
			and self.click_func is not None:
			self.click_func(self)


class ButtonGrid(object):
	def __init__(self, width, height, cols, rows):
	
		self.col_size = width / cols
		self.row_size = height / rows
		self.buttons = []

	def add(self, col, row, text, rowspan=1, colspan=1, **kwargs):
		
		x = col*self.col_size
		y = row*self.row_size
		width = colspan*self.col_size
		height = rowspan*self.row_size
		self.buttons.append(Button((x,y,width,height), text, **kwargs))

	def render(self, screen):
		
	
		for button in self.buttons:
			button.render(screen)

	def click(self, location):
	
		for button in self.buttons:
			button.click(location)
