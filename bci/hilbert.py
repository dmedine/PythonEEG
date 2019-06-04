from data_buffer import *
from process_object import process_object as po
from scipy.signal import hilbert
import numpy as np

class hilbert(po):
    def __init__(self, sr, chann_cnt, chunk_size = 64, hop_size = 1):
        po.__init__(self, sr, chann_cnt, chunk_size)
        self.out_buffer = data_buffer(chann_cnt, chunk_size=chunk_size)
        self.in_buffer = data_buffer(chann_cnt, chunk_size=chunk_size)
        # todo: check for powers of 2
        self.hop_size = hop_size
        self.shift_amnt = self.chunk_size/self.hop_size
        self.old_shift_idx = self.chunk_size-self.shift_amnt
        self.new_shift_idx = self.shift_amnt*(hop_size-1)
        self.hann = []

    def setup(self):
        hann = []
        denom = self.chunk_size - 1
        for n in range(self.chunk_size):
            hann.append(.5 * (1 - np.cos((2 * np.pi * n) / denom)))
        self.hann = np.array(hann)


    def calculate(self, frames):
        # shift
        if self.hop_size > 1:
            self.in_buffer[0:self.shift_amnt, :] = self.in_buffer[self.old_shift_idx:, :]
        self.in_buffer[self.new_shift_idx:, :] = frames
        self.out_buffer = self.in_buffer*self.hann
        self.out_buffer = hilbert(self.out_buffer)
        self.out_buffer = np.abs(self.out_buffer)

