from urllib2 import Request, urlopen, URLError
from ast import literal_eval
from time import sleep, strftime, gmtime
from os import kill, killpg, setsid
from signal import SIGINT, SIGTERM
from subprocess import Popen, PIPE


class StreamerProcess(object):

    def __init__(self, cmd, name):
        self.script = script
        self.process = Popen(cmd, stdout=PIPE, shell=True, preexec_fn=setsid)
        self.name = name
        print 'started process:', name

    def isAlive(self):
        # should return true if process is still running
        pass

    def kill(self):
        try:
            killpg(self.process.pid, SIGTERM)
            print 'killed process', self.name
            subprocesses = []
        except Exception, e:
            print 'Problem killing process:', e



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
    status = ''

    # we're connected to the internet
    if data:
        last_data = literal_eval(data)

        # display feed
        if visibility(last_data):
            status = 'connection, live feed'

            if len(subprocesses) == 0:
                iss_streamer = StreamerProcess('./iss-streamer.sh', 'iss_streamer')
                subprocesses.append(iss_streamer)

	else:
            # display ground track
            status = 'connection, ground track'
            if len(subprocesses) > 0:
	        subprocesses[0].kill()

    # no internet
    else:
        status = 'no connection'
	if len(subprocesses) > 0:
	    subprocesses[0].kill()

    print strftime("\n%a, %d %b %Y %X +0000", gmtime()), status
    try:
        print 'length: ', len(subprocesses),
        print 'pid: ', subprocesses[0].process.pid
    except:
        print 'NA\n'

    sleep(15)

subprocesses = []
if __name__ == "__main__":
    while True:
        main()
