import os, sys
import pathlib
import pyaudio
import wave
import keyboard
import time

# Change this to point to your directory containing the transcript
path = "../CalumData"

# Location of transcript and where to store audio recording data
audio_files_path = os.path.join(path, "wavs")

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second

def record(name):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    # Uncomment to view audio device indices - can add input_device_index=i as a stream constructor param
    # info = p.get_host_api_info_by_index(0)
    # numdevices = info.get('deviceCount')
    # for i in range(0, numdevices):
    #         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
    #             print ("Input Device id", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Record until keystroke
    input('Press ENTER to start recoding the line above and Enter again to stop...')
    print('Recording')
    while True:
        if keyboard.is_pressed('e'):
            break
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()
    print('Finished recording')

    filename = os.path.join(audio_files_path, "{}.wav".format(name))
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    pathlib.Path(audio_files_path).mkdir(parents=True, exist_ok=True) 
    transcript = os.path.join(path, "transcript.csv")

    for f in os.listdir(audio_files_path):
        print(f)

    # Start number in the transcript csv based on how many lines we have recorded already in our audio files
    start_line = len([name for name in os.listdir(audio_files_path)])
    print("Starting at line {}".format(start_line))

    with open(transcript, "r") as f:
        # enumerate(x) uses x.next, so it doesn't read the entire file in memory 
        for i, line in enumerate(f):
            if i >= start_line:
                os.system('cls' if os.name == 'nt' else 'clear')

                # Get the name of the new audio file and the line from the transcript it contains
                name, line, _ = line.split("|")

                # Print the line for me to read
                print("\n\n\n\n\n\n\n{0}\n{1}\n{0}\n\n\n\n\n\n".format("-"*40, line))

                # Record the line and output to Data directory
                record(name)







