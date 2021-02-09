from playsound import playsound
import time
import requests
import json
from datetime import datetime, timedelta
import os

os.system("clear")  # Automatically clears screen when programme runs


class bcolors:
  HEADER = "\033[95m"
  BLUE = "\033[94m"
  GREEN = "\033[92m"
  WARNING = "\033[93m"
  RED = "\033[91m"
  ENDC = "\033[0m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"


def playAudio(filename):
  chunk = 1024
  # wf for wave files
  wf = wave.open(filename, "rb")
  # pa for pyaudio
  pa = pyaudio.PyAudio()

  stream = pa.open(format = pa.get_format_from_width(wf.getsampwidth()),
                   channels = wf.getnchannels(),
                   rate = wf.getframerate(),
                   output = True)

  dataStream = wf.readframes(chunk)

  while dataStream != '':
    stream.write(dataStream)
    dataStream = wf.readframes(chunk)

  stream.close()
  pa.terminate()


oldPrice = 0
newPrice = 0
last_update_time = datetime.now() - timedelta(hours = 2)

while True:
  api_request = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
  api = json.loads(api_request.content)
  # 2021-02-09T10:27:00+00:00
  current_update_time = datetime.fromisoformat(api['time']["updatedISO"]).replace(tzinfo=None)
  if current_update_time > last_update_time:
    newPrice = api['bpi']['EUR']['rate_float']
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(bcolors.BOLD + bcolors.WARNING + bcolors.UNDERLINE + "< Bitcoin (BTC) >" + bcolors.ENDC)
    print(bcolors.BOLD + " * Current price: €" + str(newPrice) + "" + bcolors.ENDC)
    diff = newPrice - oldPrice
    if diff < -5:
      print(bcolors.RED + "  Price fell by €" + str(diff) + "" + bcolors.ENDC)
      playsound("./audio/napalmdeath.mp3")
    if diff >= 5 :
      print(bcolors.GREEN + "  Price rose by €" + str(diff) + "" + bcolors.ENDC)
      playsound("./audio/light.mp3")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    oldPrice = newPrice
    
  time.sleep(10)
