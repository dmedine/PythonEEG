from lsl_io import lsl_inlet, resolve_stream, lsl_outlet
from band_filter import band_filter
from pylsl import StreamInfo

global processing_chain
def process_pc(signal):
    global processing_chain
    for proc in processing_chain:
        signal = proc.process(signal)
        
block_size = 4
info = resolve_stream('type', 'EEG')
inlet = lsl_inlet(info[0],block_size=block_size, cb=process_pc)
sr = inlet.info.nominal_srate()
chann_cnt = inlet.info.channel_count()
alpha_filter = band_filter(sr, chann_cnt, band='alpha', block_size=block_size)
info = StreamInfo('lala', 'EEG', chann_cnt, sr, 'float32', 'myuid1234')
outlet = lsl_outlet(info)


processing_chain = []
processing_chain.append(alpha_filter)
#processing_chain.append(inlet)
processing_chain.append(outlet)
inlet.launch_listener()


# # init signal chain
# signal = inlet.external_data_buffer
# # automate this?
# inlet.launch_listener()
# old_time_now = 0.0
# while(1):
#     time_now = local_clock()
#     time_diff = time_now - old_time_now
#     for process in processing_chain:
#         signal = process.process(signal)
#     old_time_now = time_now
    #if inlet.external_data_buffer.new_samples>=block_size:
    #signal = inlet.process(signal)
        #signal = alpha_filter.out_buffer.read(signal)
    #outlet.process(signal)
    #else:
    #    time.sleep(.01)