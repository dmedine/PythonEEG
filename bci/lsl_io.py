from pylsl import resolve_stream, resolve_streams, StreamInlet, StreamOutlet
from data_buffer import data_buffer
import threading
import time
from process_object import  process_object as po
import numpy as np

def list_all_streams(wait_time = 1.0):
    # todo: be a little more proactive here
    infos = resolve_streams(wait_time)

def stream_query(prop, value):
    info = []
    if prop is not 'type' or 'name' or 'source_id':
        return -1
    info = resolve_stream(prop, value)
    return info


class lsl_inlet(po):
    def __init__(self, info, block_size=4, processing_flags=0, cb=None):
        self.inlet = StreamInlet(info, max_buflen=block_size, max_chunklen=block_size, processing_flags=processing_flags)
        self.info = self.inlet.info()
        po.__init__(self, self.info.nominal_srate(), self.info.channel_count(), block_size)
        self.internal_data_buffer = data_buffer(self.inlet.channel_count, block_size=block_size, block_cnt=4)
        self.internal_time_stamp_buffer = data_buffer(1, block_size=block_size, block_cnt=4)
        self.external_data_buffer = data_buffer(self.inlet.channel_count, block_size=block_size)
        self.external_time_stamp_buffer = data_buffer(1, block_size=block_size)
        self.thread = None
        self.running = False
        self._lock = threading.Lock()
        self.new_samples = 0
        self.cb = None
        self.wrt_ptr = 0
        self.rd_ptr = 0
        self.new_chunk_sz = 0
        self.cb = cb

    def __del__(self):
        self.kill_listener()

    def kill_listener(self):
        if self.running is True:
            self.running = False
            self.thread.join()

    def pull_frames(self):
        while self.running is True:
            chunk, timestamps = self.inlet.pull_chunk()
            if(len(chunk)!=0):
                self._lock.acquire()
                self.internal_data_buffer.write_raw(np.array(chunk))
                self.internal_time_stamp_buffer.write_raw(np.array([timestamps]))
                self.new_samples += len(chunk)
                self.new_chunk_sz = len(chunk)
                self.wrt_ptr = self.internal_data_buffer.wrt_ptr
                self.rd_ptr = self.rd_ptr - self.block_size
                # todo: safety check if rd_ptr < -block_size, we are in trouble...
                if self.rd_ptr < 0:
                    self.rd_ptr += self.block_size

                while self.new_samples >= self.external_data_buffer.frame_cnt:
                    frames = self.internal_data_buffer.read(self.external_data_buffer)
                    self.cb(frames)
                     #self.external_data_buffer = self.internal_data_buffer.read(self.external_data_buffer)
                     #self.external_time_stamp_buffer = self.internal_time_stamp_buffer.read(self.external_time_stamp_buffer)
                    self.new_samples-=self.external_data_buffer.frame_cnt

                self._lock.release()
            else:
                time.sleep(.01)

    def launch_listener(self):
        self.running = True
        self.thread = threading.Thread(target=self.pull_frames)
        self.thread.start()

    def process(self, frames):
        #self._lock.acquire()
        frames = self.internal_data_buffer.read(frames)
        #self._lock.release()
        return frames

class lsl_outlet(po):
    def __init__(self, info):
        self.outlet = StreamOutlet(info)

    def process(self, frames):
        if frames.chann_cnt is not self.outlet.channel_count:
            return -1
        self.outlet.push_chunk(frames.buffer.tolist())
        return frames


