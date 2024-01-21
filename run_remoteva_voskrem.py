import os

import requests
import json

import play_wav

version="1.3"

# main options
with open('options.json', 'r', encoding="utf-8") as f:
    s = f.read(10000000)
    f.close()
saved_options = json.loads(s)

ttsFormat = saved_options["ttsFormat"] # "none" (TTS on server) or "saytxt" (TTS on client)
                    # or "saywav" (TTS on server to WAV, Wav played on client)
                    # or mix of the params, splitted by , = "none,saytxt" as example
ttsFormatList = ttsFormat.split(",")
baseUrl = saved_options["baseUrl"] # server with Irene WEB api
deviceId=int(saved_options["deviceId"]) # device id
samplerateMic=int(saved_options["samplerateMic"]) # sampling rate
from urllib.parse import urlparse
urlparsed = urlparse(baseUrl)

if os.path.exists("error_connection.wav"):
    pass
else: # первый вызов, давайте получим файлы
    print("Получаем WAV-файлы, которые будут играться в случае ошибок...")

    r = requests.get(baseUrl+"ttsWav", params={"text": "Ошибка: потеряна связь с сервером"})
    res = json.loads(r.text)
    play_wav.saywav_to_file(res,'error_connection.wav')

    r = requests.get(baseUrl+"ttsWav", params={"text": "Ошибка при обработке результата сервера"})
    res = json.loads(r.text)
    play_wav.saywav_to_file(res,'error_processing.wav')

    print("WAV-файлы для ошибок получены!")


if "saytxt" in ttsFormatList:
    import pyttsx3
    ttsEngine = pyttsx3.init()
    voices = ttsEngine.getProperty("voices")
    ttsEngine.setProperty("voice", 0)


mic_blocked = False

import json
import asyncio
import websockets
import logging
import sounddevice as sd
import argparse

# ------------------- vosk ------------------
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))

async def run_test(deviceId,samplerateMic):

    with sd.RawInputStream(samplerate=samplerateMic, blocksize = 4000, device=deviceId, dtype='int16',
                           channels=1, callback=callback) as device:

        async with websockets.connect(args.uri) as websocket:
            await websocket.send('{ "config" : { "sample_rate" : %d } }' % device.samplerate)

            while True:
                data = await audio_queue.get()
                await websocket.send(data)
                #print (await websocket.recv())
                res = await websocket.recv()
                resj = json.loads(res)
                if "text" in resj:
                    voice_input_str = resj["text"]
                    #print(restext)
                    if voice_input_str != "" and voice_input_str != None:
                        print(voice_input_str)

                        try:
                            r = requests.get(baseUrl+"sendRawTxt", params={"rawtxt": voice_input_str, "returnFormat": ttsFormat})
                            if r.text != "":
                                res = json.loads(r.text)
                                if res != "NO_VA_NAME": # some cmd was run
                                    if res != None and res != "": # there is some response to play
                                        if "saytxt" in ttsFormatList:
                                            if "restxt" in res.keys():
                                                ttsEngine.say(res["restxt"])
                                                ttsEngine.runAndWait()

                                        if "saywav" in ttsFormatList:
                                            play_wav.saywav_to_file(res,'tmpfile.wav')
                                            mic_blocked = True
                                            try:
                                                play_wav.play_wav('tmpfile.wav')
                                            except Exception as e:
                                                print("Can't play received WAV")
                                            mic_blocked = False

                        except requests.ConnectionError as e:
                            play_wav.play_wav('error_connection.wav')
                        except Exception as e:
                            play_wav.play_wav('error_processing.wav')

                    else:
                        #print("2",rec.PartialResult())
                        pass


            await websocket.send('{"eof" : 1}')
            #print (await websocket.recv())

async def main():

    global args
    global loop
    global audio_queue

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(description="ASR Server",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     parents=[parser])
    parser.add_argument('-u', '--uri', type=str, metavar='URL',
                        # by default connect to WEBAPI server with PORT+1
                        help='Server URL', default='ws://{0}:{1}'.format(urlparsed.hostname,urlparsed.port+1))
    parser.add_argument('-d', '--device', type=int_or_str,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate', default=16000)
    args = parser.parse_args(remaining)
    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue()

    logging.basicConfig(level=logging.INFO)
    print("Remote Irene (VOSK REMOTE recognizer) v{0} started! ttsFormat={1}, baseUrl={2}, speechRecognizerWebsocketUrl={3}".format(version,ttsFormat,baseUrl,args.uri))
   
    print('\nAvaliable devices:')
    print(sd.query_devices())
    print()
    
    await run_test(deviceId,samplerateMic)

if __name__ == '__main__':
    asyncio.run(main())
