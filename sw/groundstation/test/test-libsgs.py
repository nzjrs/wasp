import time
import data_emitter as de

def foo(*args):
    print args

f = de._SGSSockServer('localhost',7000, foo)
f.start()

i = 10
while i:
    time.sleep(1)
    i -= 1

f.cancel()
f.join()

