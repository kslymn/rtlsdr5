from views import *


class FreqShowController(object):
	
	def __init__(self, model):
		
		self.model = model
		self.instant = InstantSpectrogram(model, self)
		self._current_view = None
		self.change_to_instant()

	def change_view(self, view):
		
		self._prev_view = self._current_view
		self._current_view = view

	def current(self):
		
		return self._current_view

	def message_dialog(self, text, **kwargs):
		
		self.change_view(MessageDialog(self.model, text, 
			cancel=self._change_to_previous, **kwargs))

	def number_dialog(self, label_text, unit_text, **kwargs):
		
		self.change_view(NumberDialog(self.model, label_text, unit_text,
			cancel=self._change_to_previous, **kwargs))

	def _change_to_previous(self, *args):
		
		self.change_view(self._prev_view)

	
	def change_to_main(self, *args):
		
		self.change_view(self._main_view)

	def toggle_main(self, *args):
		
		if self._current_view == self.waterfall:
			self.change_to_instant()
		else:
			self.change_to_waterfall()

	def change_to_instant(self, *args):
		
		self._main_view = self.instant
		self.change_view(self.instant)

	
	def change_to_settings(self, *args):
		
		self.change_view(SettingsList(self.model, self))
