import math
import sys

import numpy as np
import pygame

import freqshow
import ui


# Spectrogram renkleri.

def lerp(x, x0, x1, y0, y1):
	
	return y0 + (y1 - y0)*((x - x0)/(x1 - x0))

def rgb_lerp(x, x0, x1, c0, c1):
	
	return (math.floor(lerp(x, x0, x1, float(c0[0]), float(c1[0]))),
			math.floor(lerp(x, x0, x1, float(c0[1]), float(c1[1]))),
			math.floor(lerp(x, x0, x1, float(c0[2]), float(c1[2]))))

def gradient_func(colors):
	
	grad_width = 1.0 / (len(colors)-1.0)
	def _fun(value):
		if value <= 0.0:
			return colors[0]
		elif value >= 1.0:
			return colors[-1]
		else:
			pos = int(value / grad_width)
			c0 = colors[pos]
			c1 = colors[pos+1]
			x = (value % grad_width)/grad_width
			return rgb_lerp(x, 0.0, 1.0, c0, c1)
	return _fun

def clamp(x, x0, x1):
	
	if x > x1:
		return x1
	elif x < x0:
		return x0
	else:
		return x


class ViewBase(object):
	

	def render(self, screen):
		pass

	def click(self, location):
		pass


class MessageDialog(ViewBase):
	

	def __init__(self, model, text, accept, cancel=None):
		self.accept = accept
		self.cancel = cancel
		self.buttons = ui.ButtonGrid(model.width, model.height, 4, 5)
		self.buttons.add(3, 4, 'Kabul', click=self.accept_click, 
			bg_color=freqshow.ACCEPT_BG)
		if cancel is not None:
			self.buttons.add(0, 4, 'Iptal', click=self.cancel_click, 
				bg_color=freqshow.CANCEL_BG)
		self.label = ui.render_text(text, size=freqshow.NUM_FONT,
			fg=freqshow.BUTTON_FG, bg=freqshow.MAIN_BG)
		self.label_rect = ui.align(self.label.get_rect(),
			(0, 0, model.width, model.height))

	def render(self, screen):
		
		screen.fill(freqshow.MAIN_BG)
		self.buttons.render(screen)
		screen.blit(self.label, self.label_rect)

	def click(self, location):
		self.buttons.click(location)

	def accept_click(self, button):
		self.accept()

	def cancel_click(self, button):
		self.cancel()


        # Deger ekranindaki numaralar.

class NumberDialog(ViewBase):
	

	def __init__(self, model, label_text, unit_text, initial='0', accept=None,
		cancel=None, has_auto=False, allow_negative=False):
		
		
		self.value = str(initial)
		self.unit_text = unit_text
		self.model = model
		self.accept = accept
		self.cancel = cancel
		self.buttons = ui.ButtonGrid(model.width, model.height, 4, 5)
		self.buttons.add(0, 1, '1', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(1, 1, '2', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(2, 1, '3', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(0, 2, '4', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(1, 2, '5', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(2, 2, '6', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(0, 3, '7', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(1, 3, '8', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(2, 3, '9', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(1, 4, '0', font_size=freqshow.NUM_FONT, click=self.number_click)
		self.buttons.add(2, 4, '.', font_size=freqshow.NUM_FONT, click=self.decimal_click)
		self.buttons.add(0, 4, 'Sil', click=self.delete_click)
		if not allow_negative:
			
			self.buttons.add(3, 1, 'Temizle', click=self.clear_click)
		else:
			
			self.buttons.add(3, 1, '+/-', click=self.posneg_click)
		self.buttons.add(3, 3, 'Iptal', click=self.cancel_click,
			bg_color=freqshow.CANCEL_BG)
		self.buttons.add(3, 4, 'Kabul', click=self.accept_click,
			bg_color=freqshow.ACCEPT_BG) 
		if has_auto:
			self.buttons.add(3, 2, 'Auto', click=self.auto_click)
		
		self.input_rect = (0, 0, self.model.width, self.buttons.row_size)
		self.label = ui.render_text(label_text, size=freqshow.MAIN_FONT, 
			fg=freqshow.INPUT_FG, bg=freqshow.INPUT_BG)
		self.label_pos = ui.align(self.label.get_rect(), self.input_rect,
			horizontal=ui.ALIGN_LEFT, hpad=10)

	def render(self, screen):
		
		screen.fill(freqshow.MAIN_BG)
		screen.fill(freqshow.INPUT_BG, self.input_rect)
		screen.blit(self.label, self.label_pos)
		value_label = ui.render_text('{0} {1}'.format(self.value, self.unit_text),
			size=freqshow.NUM_FONT, fg=freqshow.INPUT_FG, bg=freqshow.INPUT_BG)
		screen.blit(value_label, ui.align(value_label.get_rect(), self.input_rect,
			horizontal=ui.ALIGN_RIGHT, hpad=-10))
		
		self.buttons.render(screen)

	def click(self, location):
		self.buttons.click(location)

	
	def auto_click(self, button):
		self.value = 'Auto'

	def clear_click(self, button):
		self.value = '0'

	def delete_click(self, button):
		if self.value == 'Auto':
			
			return
		elif len(self.value) > 1:
			
			self.value = self.value[:-1]
		else:
			
			self.value = '0'

	def cancel_click(self, button):
		if self.cancel is not None:
			self.cancel()

	def accept_click(self, button):
		if self.accept is not None:
			self.accept(self.value)

	def decimal_click(self, button):
		if self.value == 'Auto':
			
			self.value = '0.'
		elif self.value.find('.') == -1:
			
			self.value += '.'

	def number_click(self, button):
		if self.value == '0' or self.value == 'Auto':
			
			self.value = button.text
		else:
			
			self.value += button.text

	def posneg_click(self, button):
		if self.value == 'Auto':
			
			return
		else:
			if self.value[0] == '-':
				
				self.value = self.value[1:]
			else:
				
				self.value = '-' + self.value


class SettingsList(ViewBase):
	

	def __init__(self, model, controller):
		self.model      = model
		self.controller = controller
		
		centerfreq_text = 'Merkezi Frekans: {0:0.2f} MHz'.format(model.get_center_freq())
		samplerate_text = 'Sample Rate: {0:0.2f} MHz'.format(model.get_sample_rate())
		gain_text       = 'Kazanc: {0} dB'.format(model.get_gain())
		min_text        = 'Min: {0} dB'.format(model.get_min_string())
		max_text        = 'Max: {0} dB'.format(model.get_max_string())
		# Butonlarin olusumu
		self.buttons = ui.ButtonGrid(model.width, model.height, 4, 5)
		self.buttons.add(0, 0, centerfreq_text, colspan=4, click=self.centerfreq_click)
		self.buttons.add(0, 1, samplerate_text, colspan=4, click=self.sample_click)
		self.buttons.add(0, 2, gain_text,       colspan=4, click=self.gain_click)
		self.buttons.add(0, 3, min_text,        colspan=2, click=self.min_click)
		self.buttons.add(2, 3, max_text,        colspan=2, click=self.max_click)
		self.buttons.add(0, 4, 'Geri', click=self.controller.change_to_main)

	def render(self, screen):
		
		screen.fill(freqshow.MAIN_BG)
		self.buttons.render(screen)

	def click(self, location):
		self.buttons.click(location)

	# Butonlarin gorevi
	
	def centerfreq_click(self, button):
		self.controller.number_dialog('Frekans:', 'MHz',
			initial='{0:0.2f}'.format(self.model.get_center_freq()),
			accept=self.centerfreq_accept)

	def centerfreq_accept(self, value):
		self.model.set_center_freq(float(value))
		self.controller.waterfall.clear_waterfall()
		self.controller.change_to_settings()

	def sample_click(self, button):
		self.controller.number_dialog('Sample Rate:', 'MHz',
			initial='{0:0.2f}'.format(self.model.get_sample_rate()),
			accept=self.sample_accept)

	def sample_accept(self, value):
		self.model.set_sample_rate(float(value))
		self.controller.waterfall.clear_waterfall()
		self.controller.change_to_settings()

	def gain_click(self, button):
		self.controller.number_dialog('Kazanc:', 'dB',
			initial=self.model.get_gain(), accept=self.gain_accept, 
			has_auto=True)

	def gain_accept(self, value):
		self.model.set_gain(value)
		self.controller.waterfall.clear_waterfall()
		self.controller.change_to_settings()

	def min_click(self, button):
		self.controller.number_dialog('Min:', 'dB',
			initial=self.model.get_min_string(), accept=self.min_accept, 
			has_auto=True, allow_negative=True)

	def min_accept(self, value):
		self.model.set_min_intensity(value)
		self.controller.waterfall.clear_waterfall()
		self.controller.change_to_settings()

	def max_click(self, button):
		self.controller.number_dialog('Max:', 'dB',
			initial=self.model.get_max_string(), accept=self.max_accept, 
			has_auto=True, allow_negative=True)

	def max_accept(self, value):
		self.model.set_max_intensity(value)
		self.controller.waterfall.clear_waterfall()
		self.controller.change_to_settings()

# Program Ana Ekran

class SpectrogramBase(ViewBase):
	

	def __init__(self, model, controller):
		self.model      = model
		self.controller = controller
		self.buttons = ui.ButtonGrid(model.width, model.height, 4, 5)
		self.buttons.add(0, 0, 'Ayarlar', click=self.controller.change_to_settings)
		self.buttons.add(1, 0, 'Mod', click=self.controller.toggle_main, colspan=2)
		self.buttons.add(3, 0, 'Cikis', click=self.quit_click,
			bg_color=freqshow.CANCEL_BG)
		self.overlay_enabled = True

	def render_spectrogram(self, screen):
		
		raise NotImplementedError

	def render_hash(self, screen, x, size=5, padding=2):
		
		y = self.model.height - self.buttons.row_size + padding
		pygame.draw.lines(screen, freqshow.BUTTON_FG, False, 
			[(x, y), (x-size, y+size), (x+size, y+size), (x, y), (x, y+2*size)])

	def render(self, screen):
		
		screen.fill(freqshow.MAIN_BG)
		if self.overlay_enabled:
			
			spect_rect = (0, self.buttons.row_size, self.model.width,
				self.model.height-2*self.buttons.row_size)
			self.render_spectrogram(screen.subsurface(spect_rect))
			self.render_hash(screen, 0)
			self.render_hash(screen, self.model.width/2)
			self.render_hash(screen, self.model.width-1)
			bottom_row  = (0, self.model.height-self.buttons.row_size,
				self.model.width, self.buttons.row_size)
			freq        = self.model.get_center_freq()
			bandwidth   = self.model.get_sample_rate()
			label = ui.render_text('{0:0.2f} Mhz'.format(freq-bandwidth/2.0),
				size=freqshow.MAIN_FONT)
			screen.blit(label, ui.align(label.get_rect(), bottom_row,
				horizontal=ui.ALIGN_LEFT))
			label = ui.render_text('{0:0.2f} Mhz'.format(freq),
				size=freqshow.MAIN_FONT)
			screen.blit(label, ui.align(label.get_rect(), bottom_row,
				horizontal=ui.ALIGN_CENTER))
			
			label = ui.render_text('{0:0.2f} Mhz'.format(freq+bandwidth/2.0),
				size=freqshow.MAIN_FONT)
			screen.blit(label, ui.align(label.get_rect(), bottom_row,
				horizontal=ui.ALIGN_RIGHT))
			
			label = ui.render_text('{0:0.0f} dB'.format(self.model.min_intensity),
				size=freqshow.MAIN_FONT)
			screen.blit(label, ui.align(label.get_rect(), spect_rect,
				horizontal=ui.ALIGN_LEFT, vertical=ui.ALIGN_BOTTOM))
			
			label = ui.render_text('{0:0.0f} dB'.format(self.model.max_intensity),
				size=freqshow.MAIN_FONT)
			screen.blit(label, ui.align(label.get_rect(), spect_rect,
				horizontal=ui.ALIGN_LEFT, vertical=ui.ALIGN_TOP))
			
			self.buttons.render(screen)
		else:
			
			self.render_spectrogram(screen)

	def click(self, location):
		mx, my = location
		if my > self.buttons.row_size and my < 4*self.buttons.row_size:
			
			self.overlay_enabled = not self.overlay_enabled
		else:
			
			self.buttons.click(location)

	def quit_click(self, button):
		self.controller.message_dialog('Cikis',
			accept=self.quit_accept)

	def quit_accept(self):
		sys.exit(0)

class WaterfallSpectrogram(SpectrogramBase):


	def __init__(self, model, controller):
		super(WaterfallSpectrogram, self).__init__(model, controller)
		self.color_func = gradient_func(freqshow.WATERFALL_GRAD)
		self.waterfall = pygame.Surface((model.width, model.height))

	def clear_waterfall(self):
		self.waterfall.fill(freqshow.MAIN_BG)

	def render_spectrogram(self, screen):
	
		freqs = self.model.get_data()
		self.waterfall.scroll(0, -1)
		
		freqs = (freqs-self.model.min_intensity)/self.model.range
	
		x, y, width, height = screen.get_rect()
		wx, wy, wwidth, wheight = self.waterfall.get_rect()
		offset = wheight - height
	
		self.waterfall.lock()
		for i in range(width):
			power = clamp(freqs[i], 0.0, 1.0)
			self.waterfall.set_at((i, wheight-1), self.color_func(power))
		self.waterfall.unlock()
		screen.blit(self.waterfall, (0, 0), area=(0, offset, width, height))

class InstantSpectrogram(SpectrogramBase):
	

	def __init__(self, model, controller):
		super(InstantSpectrogram, self).__init__(model, controller)

	def render_spectrogram(self, screen):
		
		freqs = self.model.get_data()
		
		x, y, width, height = screen.get_rect()
		freqs = height-np.floor(((freqs-self.model.min_intensity)/self.model.range)*height)
		
		screen.fill(freqshow.MAIN_BG)
		
		ylast = freqs[0]
		for i in range(1, width):
			y = freqs[i]
			pygame.draw.line(screen, freqshow.INSTANT_LINE, (i-1, ylast), (i, y))
			ylast = y
