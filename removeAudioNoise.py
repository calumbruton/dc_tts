import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib
import os
import pathlib
import subprocess

# Location of transcript and where to store audio recording data
input_dir = "../CalumData/wavs"
output_dir = "../CalumData/denoisedWavs"
base_dir = "../CalumData"

# from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0)) 
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize

# from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8 # unsigned char
    elif sample_width == 2:
        dtype = np.int16 # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels



if __name__ == '__main__':

    # Create output directory if it doesn't exist
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True) 

    # For each wav file in the input dir
    for fname in os.listdir(input_dir):

        # The full file input and output paths
        file_input_path = os.path.join(input_dir, fname)
        file_output_path = os.path.join(output_dir, fname)
        noise_prof_path = os.path.join(base_dir, 'noise.prof')

        print(file_input_path, file_output_path, noise_prof_path)

        # Remove noise using sox - must be in PATH
        res = subprocess.Popen(['sox', file_input_path, file_output_path, 'noisered', noise_prof_path, '0.21'], shell = True)
















        # with wave.open(file_input_path,'rb') as spf:
            # cutOffFrequency = 400.0
            # sampleRate = spf.getframerate()
            # ampWidth = spf.getsampwidth()
            # nChannels = spf.getnchannels()
            # nFrames = spf.getnframes()

            # print(sampleRate, ampWidth, nChannels, nFrames)

            # # Extract Raw Audio from multi-channel Wav File
            # signal = spf.readframes(nFrames*nChannels)
            # spf.close()
            # channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)


            # Low Pass Filter -------------------------------
            # get window size
            # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
            # freqRatio = (cutOffFrequency/sampleRate)
            # N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)

            # Use moviung average (only on first channel)
            # filtered = running_mean(channels[0], N).astype(channels.dtype)
            # End of Low Pass Filter -------------------------------

            # Reduce noise ----------------------


            # channels[0] = [x if x>250 or x<-250 else 0 for x in channels[0]]
            # print(len(channels[0]))
            
            # Clip some off the beginning and end
            # channel_clipped = channels[0][20000:len(channels[0])-10000]

            # Write out wav file
            # wav_file = wave.open(file_output_path, "w")
            # wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
            # wav_file.writeframes(channels[0].tobytes('C'))
            # wav_file.close()