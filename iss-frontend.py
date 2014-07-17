from urllib2 import Request, urlopen, URLError
from ast import literal_eval
from time import sleep, strftime, gmtime
from os import kill, killpg, setsid
from signal import SIGINT, SIGTERM
from subprocess import Popen, PIPE


class StreamerProcess(object):

    def __init__(self, cmd, name):
        global subprocesses
        self.process = Popen(cmd, stdout=PIPE, shell=True, preexec_fn=setsid)
        self.name = name
        print '+' * 30
        print 'started process:', name
        print '+' * 30

    def isAlive(self):
        # should return true if process is still running
        pass

    def kill(self):
        global subprocesses
        try:
            killpg(self.process.pid, SIGTERM)
            print '-' * 30
            print 'killed process', self.name
            print '-' * 30
            subprocesses = []
        except Exception, e:
            print 'Problem killing process:', e

def streamer(cmd, name = None):
    global subprocesses

    if len(subprocesses) < 1:
        subprocess = StreamerProcess(cmd, name)
        subprocesses.append(subprocess)
    elif subprocesses[0].name != name:
        subprocesses[0].kill()
        subprocess = StreamerProcess(cmd, name)
        subprocesses.append(subprocess)

def get_data():
    # api request
    request = Request('https://api.wheretheiss.at/v1/satellites/25544')

    # hit the whereistheiss server to find current info
    try:
        response = urlopen(request, timeout=1)
        data = response.read()
        return data
    except URLError, e:
        print 'No API data. Got an error code:', e
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

    # plenty of internet
    if data:
        last_data = literal_eval(data)

        # display feed
        if visibility(last_data):
            streamer('./iss-streamer.sh', 'hd iss streamer')

        # display ground track
        else:
            streamer('./old-iss-streamer.sh', 'old iss streamer')

    # no internet
    else:
        streamer('')

    print strftime("\n%a, %d %b %Y %X +0000", gmtime())
    try:
        print 'process running: %s, pid: %d' % (subprocesses[0].name, subprocesses[0].process.pid)
    except:
        print 'An error occurred, no process is '

    sleep(15)

subprocesses = []
if __name__ == "__main__":
    while True:
        main()
