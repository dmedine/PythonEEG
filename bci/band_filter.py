from data_buffer import *
import numpy as np
from scipy.signal import butter, lfilter
from process_object import process_object as po
import time

from threading import Thread, Lock

class band_filter(po):
    def __init__(self, sr, chann_cnt, block_size=4, band='alpha'):
        po.__init__(self, sr, chann_cnt, block_size)

        self.out_buffer = data_buffer(chann_cnt, block_size=block_size)
        self.tmp_array = np.array([[0.0 for i in xrange(chann_cnt)] for j in xrange(block_size)])
        self.order = 5
        self.freq_bands = {'delta': (1.0, 4.0),
                           'theta': (4.0, 8.0),
                           'alpha': (8.0, 14.0),
                           'beta': (14.0, 20.0)}

        self.nyq = .5*float(sr)
        self.coeffs = []
        self.zs = []
        self.band = band
        self.setup()

    def setup(self):

        low = self.freq_bands[self.band][0]/self.nyq
        high = self.freq_bands[self.band][1]/self.nyq
        [b, a] = butter(self.order, [low, high], btype='bandpass')
        self.coeffs = [b, a]
        state_len = max([len(a), len(b)])-1
        self.zs = np.array([[0.0 for i in xrange(self.chann_cnt)] for j in xrange(state_len)])

    def process(self, frames):
        for n in range(self.chann_cnt):
            #self.out_buffer.buffer[:, n] = lfilter(self.coeffs[0], self.coeffs[1], frames[:, n])
            self.tmp_array[:,n], self.zs[:,n] = lfilter(self.coeffs[0], self.coeffs[1], frames.buffer[:,n], zi=self.zs[:,n])
        self.out_buffer.write_raw(self.tmp_array)
        return self.out_buffer
