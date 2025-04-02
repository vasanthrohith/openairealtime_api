import sounddevice as sd
import numpy as np
import keyboard  # For detecting key press
import wave

# Audio settings
SAMPLE_RATE = 16000  # 16 kHz
CHANNELS = 1
BLOCKSIZE = 1024  # Frames per chunk

# Output file
OUTPUT_FILE = "output.wav"

def record_audio():
    print("Press and hold SPACE to record. Release to stop.")
    frames = []
    
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32', blocksize=BLOCKSIZE) as stream:
        while keyboard.is_pressed("space"):
            audio_chunk, _ = stream.read(BLOCKSIZE)
            frames.append(audio_chunk.copy())
    
    print("Recording stopped.")
    return frames

# Start recording on key press
while True:
    keyboard.wait("space")  # Wait until spacebar is pressed
    recorded_frames = record_audio()
    
    # Convert to numpy array and save as WAV
    audio_data = np.concatenate(recorded_frames, axis=0)
    audio_data = (audio_data * 32767).astype(np.int16)  # Convert to PCM 16-bit
    
    with wave.open(OUTPUT_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    
    print(f"Saved recording as {OUTPUT_FILE}")
    break  # Exit after one recording
