"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover)
info = StreamInfo('simple', 'EEG', 2, 100, 'int32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)
val1 = 0
val2 = 10
print("now sending data...")
while True:
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    mysample = [val1, val2] 
    # now send it and wait for a bit
    outlet.push_sample(mysample)
    val1 += 1
    val2 += 1
    if val1 > 9:
        val1 = 0
        val2 = 10
    time.sleep(0.01)
