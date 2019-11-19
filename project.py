# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------
LED Music Visualizer
--------------------------------------------------------------------------
License:   
Copyright 2019 Juliana Wang

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Control LED strip with WAV file data
    
    *LED strip: +5V to P1.24, Din to P1.08, and GND to P1.22
    *microUSB breakout board: Vcc to P1.07, D- to P1.09, D+ to P1.11, and GND to P.13 (P.105 and P.107 are connected by solder, P1.13 and P1.15 are connected by solder)
    *microUSB-to-USB adapter attached to USB audio splitter attached to microUSB breakout board
    *Audio splitter: Mic input can use an AUX cord, Playback can use AUX to speakers or earphones
  
LED lights according to tuple values extracted from wav file

--------------------------------------------------------------------------
Background Information: 
 
  * Setting up the LED strip:
  https://markayoder.github.io/PRUCookbook/01case/case.html#_neopixels_5050_rgb_leds_with_integrated_drivers_ledscape (Section 1.3. NeoPixels - 5050 RGB LEDs with Integrated Drivers (LEDScape))
  
  * Unpacking and analyzing wav file:
  https://stackoverflow.com/questions/2226853/interpreting-wav-data (Comment by SapphireSun on Feb 9 '10 at 6:18)
  
"""

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# PART 1: READ/UNPACK WAV FILE DATA
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

import wave
import struct

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def pcm_channels(wave_file):
    """Given a file-like object or file path representing a wave file,
    decompose it into its constituent PCM data streams.

    Input: A file like object or file path
    Output: A list of lists of integers representing the PCM coded data stream channels
        and the sample rate of the channels (mixed rate channels not supported)
    """
    global integer_data
    stream = wave.open(wave_file,"rb")

    num_channels = stream.getnchannels()
    sample_rate = stream.getframerate()
    sample_width = stream.getsampwidth()
    num_frames = stream.getnframes()

    raw_data = stream.readframes( num_frames ) # Returns byte data
    stream.close()

    total_samples = num_frames * num_channels

    if sample_width == 1: 
        fmt = "%iB" % total_samples # read unsigned chars
    elif sample_width == 2:
        fmt = "%ih" % total_samples # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    integer_data = struct.unpack(fmt, raw_data)
    del raw_data # Keep memory tidy (who knows how big it might be)

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

pcm_channels('/var/lib/cloud9/ENGI301/LEDscape/test.wav')

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# PART 2: TRIGGER LED LIGHT STRIP WITH WAV DATA
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

import time
import opc

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

ADDRESS = 'localhost:7890'

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

client = opc.Client(ADDRESS)
stop_time = time.time() + 20
STR_LEN = 240

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

integer_data = []

leds = [(0, 0, 0)] * STR_LEN    #Initializes LED array of 0's

for i in range(STR_LEN):
    leds[i] = (0,0,abs(integer_data[i]))    #Initializes LED color

Offset = 0  #Initializes Offset value, or how much to shift the pixel over
arraylength = 5000  #Set number instead of len(integer_data) to prevent accidental shutdown


while time.time() < stop_time:
    
    for i in range(STR_LEN):
        datavalue = abs(integer_data[(i+Offset)])
        leds[i] = (datavalue,datavalue,datavalue)   #Changes RGB numerical value to the value at integer_data[i]

    Offset = (Offset + 240) % arraylength   #Leaves remainder number of pixels to shift
    
    if client.put_pixels(leds, channel=0):
        pass
    
    time.sleep(0.1)
