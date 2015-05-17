import numpy as np
from rtlsdr import *

import freqshow


class FreqShowModel(object):
	def __init__(self, width, height):
		
		
		self.width = width
		self.height = height
		self.min_auto_scale = True
		self.max_auto_scale = True
		self.set_min_intensity('AUTO')
		self.set_max_intensity('AUTO')
		# RTL-SDR Kutuphanesini yukluyoruz.
		self.sdr = RtlSdr()
		self.set_center_freq(90.3)
		self.set_sample_rate(2.4)
		self.set_gain('AUTO')

	def _clear_intensity(self):
		if self.min_auto_scale:
			self.min_intensity = None
		if self.max_auto_scale:
			self.max_intensity = None
		self.range = None


        # Frekans ayarlanmasi ve setlenmesi.


	def get_center_freq(self):
		
		return self.sdr.get_center_freq()/1000000.0

	def set_center_freq(self, freq_mhz):
		
		try:
			self.sdr.set_center_freq(freq_mhz*1000000.0)
			self._clear_intensity()
		except IOError:
			
			pass

        # Sample Rate ayarlanmasi ve setlenmesi.

        
	def get_sample_rate(self):
		
		return self.sdr.get_sample_rate()/1000000.0

	def set_sample_rate(self, sample_rate_mhz):
		
		try:
			self.sdr.set_sample_rate(sample_rate_mhz*1000000.0)
		except IOError:
			
			pass

        # Kazancin ayarlanmasi ve setlenmesi. 


	def get_gain(self):
		
		if self.auto_gain:
			return 'AUTO'
		else:
			return '{0:0.1f}'.format(self.sdr.get_gain())

	def set_gain(self, gain_db):
		
		if gain_db == 'AUTO':
			self.sdr.set_manual_gain_enabled(False)
			self.auto_gain = True
			self._clear_intensity()
		else:
			try:
				self.sdr.set_gain(float(gain_db))
				self.auto_gain = False
				self._clear_intensity()
			except IOError:
				
				pass

        # Maksimum ve Minimum kullanilacak guc.


	def get_min_string(self):
		
		if self.min_auto_scale:
			return 'AUTO'
		else:
			return '{0:0.0f}'.format(self.min_intensity)

	def set_min_intensity(self, intensity):
		
		if intensity == 'AUTO':
			self.min_auto_scale = True
		else:
			self.min_auto_scale = False
			self.min_intensity = float(intensity)
		self._clear_intensity()

	def get_max_string(self):
		
		if self.max_auto_scale:
			return 'AUTO'
		else:
			return '{0:0.0f}'.format(self.max_intensity)

	def set_max_intensity(self, intensity):
		
		if intensity == 'AUTO':
			self.max_auto_scale = True
		else:
			self.max_auto_scale = False
			self.max_intensity = float(intensity)
		self._clear_intensity()

        # Spektrogram icin FFT Hesaplanmasi


	def get_data(self):
		
		
		samples = self.sdr.read_samples(freqshow.SDR_SAMPLE_SIZE)[0:self.width+2]
		freqs = np.absolute(np.fft.fft(samples))
		freqs = freqs[1:-1]
		freqs = np.fft.fftshift(freqs)
		freqs = 20.0*np.log10(freqs)
		
		if self.min_auto_scale:
			min_intensity = np.min(freqs)
			self.min_intensity = min_intensity if self.min_intensity is None \
				else min(min_intensity, self.min_intensity)
		if self.max_auto_scale:
			max_intensity = np.max(freqs)
			self.max_intensity = max_intensity if self.max_intensity is None \
				else max(max_intensity, self.max_intensity)
		
		self.range = self.max_intensity - self.min_intensity
		
		return freqs
