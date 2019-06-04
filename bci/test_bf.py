from band_filter import band_filter as bf
from data_buffer import data_buffer as db
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import lfilter, butter
sr = 250
chann_cnt = 3
samp_cnt = 256
freq = 10
per = sr/freq
filter = bf(sr, chann_cnt)
[b, a] = butter(5, [8.0/125.0, 14.0/125.0], btype='bandpass')
#data = np.array([[1.0 for i in xrange(chann_cnt)] for j in xrange(samp_cnt)])
#data[::per] = -1.0
data = np.array([[0.0 for i in xrange(chann_cnt)] for j in xrange(samp_cnt)])
data[0, :] = 1.0
output = db(chann_cnt, block_cnt=4)
#plt.plot(data[:, 0])

#plt.show()
buff = data
result = []#np.array([[0.0 for i in xrange(chann_cnt)] for j in xrange(64)])
for i in range(4):
    start_idx = i*64
    end_idx = start_idx+64
    data_in = data[start_idx:end_idx,:]
    filter.calculate(data_in)
    output.write(filter.out_buffer.buffer)

plt.plot(data[:, 0])
plt.plot(output.buffer[:, 0])
plt.show()
