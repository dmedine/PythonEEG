class process_object:
    def __init__(self, sr, chann_cnt, block_size):
        self.chann_cnt = chann_cnt
        self.block_size = block_size
        self.sr = sr
        self.out_buffer = None



