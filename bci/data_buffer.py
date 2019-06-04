import numpy as np
import time

class data_buffer:
    def __init__(self, chann_cnt, block_size=4, block_cnt=1, delay=1, ):
        self.chann_cnt = chann_cnt
        self.frame_cnt = block_cnt*block_size
        self.chIdx = 0
        self.buffer = np.array([[0.0 for k in xrange(self.chann_cnt)] for j in xrange(self.frame_cnt)])
        self.rd_ptr = 0
        self.wrt_ptr = 0
        self.delay = delay*block_size
        self.block_size = block_size
        self.block_cnt = block_cnt
        self.block_ptr = 0
        self.new_samples = 0

    def __len__(self):
        l = len(self.buffer[:,0])
        return l

    def write_raw(self, frames, channs=0, advance_wrt_ptr=True):
        # todo: check chunk size
        l = len(frames)
        wrt_ptr = self.wrt_ptr
        block_ptr = self.block_ptr
        # todo: handle buffer wrapping more elegantly
        for n in range(l):

            if channs is 0:
                self.buffer[wrt_ptr, 0:self.chann_cnt] = frames[n, 0:self.chann_cnt]
            # todo: check channel ranges
            else:
                for ch in channs:
                    self.buffer[wrt_ptr, ch] = frames[n, ch]
            wrt_ptr += 1
            self.new_samples += 1
            if wrt_ptr % self.block_size > 0:
                block_ptr += 1
                if block_ptr >= self.block_cnt:
                    block_ptr = 0
            if wrt_ptr >= self.frame_cnt:
                wrt_ptr -= self.frame_cnt
        if advance_wrt_ptr is True:
            self.wrt_ptr = wrt_ptr

    def write(self, frames, channs=0, frames_to_read=0, advance_wrt_ptr=True):
        # todo: check chunk size
        l = len(frames)
        if frames_to_read is not 0:
            l=frames_to_read
        wrt_ptr = self.wrt_ptr
        block_ptr = self.block_ptr
        # todo: handle buffer wrapping more elegantly
        for n in range(l):
            if channs is 0:
                self.buffer[wrt_ptr, 0:self.chann_cnt] = frames.buffer[n+frames.rd_ptr, 0:self.chann_cnt]
            # todo: check channel ranges
            else:
                for ch in channs:
                    self.buffer[wrt_ptr, ch] = frames.buffer[n+frames.rd_ptr, ch]
            wrt_ptr += 1
            self.new_samples += 1
            if wrt_ptr >= self.frame_cnt:
                wrt_ptr -= self.frame_cnt
        if advance_wrt_ptr is True:
            self.wrt_ptr = wrt_ptr

    def read(self, frames, channs=0, frames_to_read=0,advance_rd_ptr=True, wait_for_samples=True):
        frame_cnt = len(frames)
        if frames_to_read is not 0:
            frame_cnt = frames_to_read
        new_samples = self.new_samples
        # I think this means that I will never not have new samples to read???
        #if wait_for_samples is True:
        #    while new_samples - frames_to_read >= 0:
        #        time.sleep(.005)
        #        new_samples = self.new_samples
        # todo: handle buffer wrapping more elegantly by checking lengths
        rd_ptr = self.rd_ptr
        frames.write(self, channs=channs, frames_to_read=frame_cnt)
        rd_ptr += frame_cnt
        # todo: error checking, this should never be lt 0
        self.new_samples-=frame_cnt
        while rd_ptr >= self.frame_cnt:
           rd_ptr -= self.frame_cnt
        if advance_rd_ptr is True:
            self.rd_ptr = rd_ptr
        return frames

