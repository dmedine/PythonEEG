# # from pylsl import StreamInlet, resolve_stream
# #
# # # first resolve an EEG stream on the lab network
# # print("looking for an EEG stream...")
# # streams = resolve_stream('type', 'EEG')
# #
# # # create a new inlet to read from the stream
# # inlet = StreamInlet(streams[0])
# #
# #
# #
# # while 1:
# #     chunk, timestamps = inlet.pull_chunk()
# #
# #     if len(chunk) is not 0:
# #         print(chunk[0])
# #
# #
# #         break
# #
# import numpy as np
# from scipy.signal import butter, lfilter
# freq_bands = {'delta': (1, 4),
#                            'theta': (4, 8),
#                            'alpha': (8, 14),
#                            'beta': (14, 20)}
# nyq = 200
# order = 5
# zs = []
# for band in freq_bands.keys():
#     low = freq_bands[band][0] / nyq
#     high = freq_bands[band][1] / nyq
#     [b, a] = butter(order, [low, high], btype='band')
#     coeffs = [b, a]
#     coeffs.append(coeffs)
#     #b_sz = b.size
#     #m = max(b.size, a.size)
#     #l = len(m)
#     #l -= 1
#     z = np.array([0 for i in xrange(max(b.size, a.size))])
#     #z = np.array([0 for i in xrange(len(max(b, a)) - 1)])
#     zs.append(z)
#
# print zs
# foo = 1

from band_filter import band_filter as bf
import numpy as np
from scipy.signal import butter, lfilter
from matplotlib import pyplot as plt
[b,a] = butter(5, [8.0/125.0,14.0/125.0], btype='bandpass')
sr = 250
chann_cnt = 3
samp_cnt = 256
freq = 10
per = sr/freq
filter = bf(sr, chann_cnt)
data = np.array([[0.0 for i in xrange(chann_cnt)] for j in xrange(samp_cnt)])
data[0, :] = 1.0
z = np.array([0.0 for i in xrange(10)])
y=[]
y0,z = lfilter(b, a, data[0:63,0], zi=z)
y.append(y0)
y1,z = lfilter(b, a, data[64:127,0], zi=z)
y.append(y1)
y2,z = lfilter(b, a, data[128:191,0], zi=z)
y.append(y2)
y3,z = lfilter(b, a, data[192:255,0], zi=z)
y.append(y3)
out = np.array(y)
plt.plot(data[:,0])
plt.plot(y)
plt.show()
