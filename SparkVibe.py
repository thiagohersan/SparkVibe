#! /usr/bin/env python

from sys import exit
from os import remove
from time import time, sleep, strptime
from calendar import timegm
from urllib import urlretrieve
from urllib2 import Request, urlopen
import imp

SPARK_DEVICE = '48ff71065067555032502387'
SPARK_TOKEN = 'c54b20eb4737227bd4654dc2b7f56d8acf2ceb4e'

if __name__ == '__main__':
    urlretrieve('http://tinyurl.com/fbconsole-py', '.fbconsole.py')
    fb = imp.load_source('fb', '.fbconsole.py')
    fb.AUTH_SCOPE = ['read_mailbox']
    fb.authenticate()

    lastPokeCheck = time()
    mostRecentPoke = 0

    try:
        while(True):
            if(time()-lastPokeCheck > 1):
                lastPokeCheck = time()
                for poke in fb.graph("/me/pokes", {"since":str(mostRecentPoke)})['data']:
                    print "calling poke function with \'%s\'" % poke['from']['name']
                    req = Request("https://api.spark.io/v1/devices/"+SPARK_DEVICE+"/poke")
                    req.add_header('Authorization', "Bearer "+SPARK_TOKEN)
                    res = urlopen(req, "args="+poke['from']['name'])
                    print res.read()
                    mostRecentPoke = max(mostRecentPoke, timegm(strptime(poke['created_time'], "%Y-%m-%dT%H:%M:%S+0000")))
            sleep(0.02)
    except KeyboardInterrupt:
        remove('.fb_access_token')
        exit(0)
