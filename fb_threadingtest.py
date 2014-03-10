#!/usr/bin/env python
# Testar threading lidegranna

from threading import Thread
from sys import argv
import os

NUMTHREADS = 40

class TestThread(Thread):
    filename = ""
    numruns = 0
    finished = False
    items = []
    def run(self):
        print self.getName(),"running!"
        self.numruns = self.numruns+1
        if nextItem(self.items):
            self.filename = self.items.pop()
            os.system('/usr/bin/time -p -o ettan_tid'+str(self.numruns)+' vmatch -dnavsprot 11 -complete -h 2 -q '+self.filename+' ~/softwareevaluation/ardb > ettan_run_'+str(self.numruns))
            print "T1 finished with",t1.filename
        else:
            self.finished = True

class SecondTestThread(Thread):
    filename = ""
    numruns = 0
    finished = False
    items = []
    def run(self):
        print "T2 running!"
        self.numruns = self.numruns+1
        if nextItem(self.items):
            self.filename = self.items.pop()
            os.system('vmatch -dnavsprot 11 -complete -h 5p  -q '+self.filename+' ~/softwareevaluation/ardb > tvaan_run_'+str(self.numruns))
            print "T2 finished with",t2.filename
        else:
            self.finished = True

def nextItem(checklist):
    """Checks for another item to run"""
    if len(checklist) > 1:
        return True
    else:   
        return False


# Initalize the two threads
#t1 = TestThread()
#t2 = SecondTestThread()

# Arrange for setting filenames from argv
#t1.items = argv[1:] #everything but scriptname
#t2.items = argv[:0:-1] #reverse everything but scriptname


# Start the number of wanted threads
for i in xrange(1,NUMTHREADS+1):
    init = 't'+str(i)+'=TestThread()'
    exec init
    exec 't'+str(i)+'items = argv[1:]'
    exec 't'+str(i)+'.start()'


# Continous loop where each thread is run once for each input file, each popping
# a new item from their list until they are all done...
while True:
    for i in xrange(1,NUMTHREADS+1):
        if eval("t"+str(i)+".finished"):
            exec 't'+str(i)+'.run()'
        elif eval('t'+str(i)+'.finished'):
            pass


print "Done!"
