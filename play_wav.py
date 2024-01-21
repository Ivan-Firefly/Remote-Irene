import soundfile as sf
import sounddevice as sd

def play_wav(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

def saywav_to_file(saywav_result,wavfile):
    import save_wav
    save_wav.saywav_to_file(saywav_result,wavfile)
