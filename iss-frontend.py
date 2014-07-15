from urllib2 import Request, urlopen, URLError
from ast import literal_eval 
from time import sleep, strftime, gmtime
from os import kill, killpg, setsid
from signal import SIGINT, SIGTERM
from subprocess import Popen, PIPE

def get_data():
  # api request
  request = Request('https://api.wheretheiss.at/v1/satellites/25544')

  # hit the whereistheiss server to find current info
  try:
    response = urlopen(request, timeout = 1)
    data = response.read()
    return data
  except URLError, e:
      print 'No data. Got an error code:', e
      return False

def visibility(last_data):
  if last_data['visibility'] == 'daylight':
    return True
  else:
    return False

def main():
  global subprocesses

  # try to get the visibility data
  data = get_data()
  status = ''

  # we're connected to the internet
  if data:
    last_data = literal_eval(data)

    # display feed
    if visibility(last_data):
      status = 'connection, live feed'

      if len(subprocesses) == 0:
        live_feed = Popen("./iss-streamer.sh", stdout=PIPE, shell=True, preexec_fn=setsid) 
        subprocesses.append(live_feed)
        print 'started a process'

    # display ground track
    else:
      status = 'connection, ground track'

      try:
        killpg(subprocesses[0].pid, SIGTERM)
        print 'killed a process1'
        subprocesses = []
      except Exception, e:
        print 1, e

  # no internet
  else:
    status = 'no connection'  

    try:
      killpg(subprocesses[0].pid, SIGTERM)
      print 'killed a process2'
      subprocesses = []
    except Exception, e:
      print 2, e

  print strftime("\n%a, %d %b %Y %X +0000", gmtime()), status
  try:
    print 'length: ', len(subprocesses),
    print 'pid: ', subprocesses[0].pid
  except:
    pass
    
  sleep(15)

subprocesses = []
if __name__ == "__main__":
  while True:
      main()
      