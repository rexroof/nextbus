#!/usr/bin/python

import thread
import time
import requests


class NextBus:
   'tracks time as string or seconds'

   def __init__(self, _init=0):
       if isinstance(_init, basestring):
           self.setString(_init)
       else:
           self.setTime(_init)

   # tick by one second
   def tick(self):
     if self.seconds > 0:
       self.seconds -= 1
     return True

   # set time in seconds
   def setTime(self, _sec):
     self.seconds = _sec

   # get time in seconds
   def getTime(self):
     return self.seconds

   # set time with 00:10:00 style string
   def setString(self, _string='0:00:00'):
     _arr = _string.split(':')
     _sec = 0
     _multi = [1,60,3600]
     # using this way to avoid datetime external modules
     while _arr:
       bit = int(_arr.pop())
       mult = int(_multi.pop(0))
       _sec += (bit*mult)
     self.seconds = _sec
   
   # return time in 00:10:00 style string
   def getString(self):
     _multi = [1,60,3600]
     _secs = self.seconds
     bits = []
     # using this way to avoid datetime external modules
     while _multi:
         mult = int(_multi.pop())
         seg = int(_secs / mult)
         _secs -= int(seg * mult)
         bits.append(seg)
     return ':'.join(map(lambda b: "{:02d}".format(b), bits))
# end class NextBus
#

# this function just loops, checking the API on an interval 
#  and updating our shared NextBus object. 
def update_time(nextbus, interval=15):
    params = { 'bus': 31, 'stop': 2091, }
    url = 'https://obfuscated.execute-api.us-west-2.amazonaws.com/eta/'
    previous_time = ''
    while True:
        r = requests.get(url, params=params)
        # TODO: add error checking.  TypeError
        received = r.json()["time"]
        if received == previous_time:
            print "time was the same"
            pass
        else:
            nextbus.setString(received)
            print "set time to {}".format(received)
            previous_time = received
        time.sleep(interval)


# begin.
# initialize with expected time of 1 hr
nextbus = NextBus(3600)

thread.start_new_thread( update_time, (nextbus, 30) )

while True:
    # print time.
    print(nextbus.getString())
    # sleep 1 second
    time.sleep(1)
    # remove one second from the time
    nextbus.tick()
