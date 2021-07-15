import sys

from screen import run_all
from screen import play_sound
import multiprocessing
from multiprocessing import Manager
import config

config.init()
mylist = [ False]

def soundmanager(num):
    p3 = multiprocessing.Process(target=play_sound)
    p3.start()
    count = 1
    # p3.terminate()
    while(True):
        if num.value == 1:
            p3.terminate()
            count -= 1
            num.value = 2
        if num.value == 0 and count == 0:
            p3 = multiprocessing.Process(target=play_sound)
            p3.start()
            num.value = 2
            count += 1


def processManager():
    manager = Manager()
    num = manager.Value('i', 2)
    finish = manager.Value('i',0)

    p1 = multiprocessing.Process(target=run_all, args=(num,finish,))
    p2 = multiprocessing.Process(target=soundmanager, args=(num,))
    p1.start()
    p2.start()
    while(True):
        if finish.value == 1:
            p1.terminate()
            p2.terminate()
            sys.exit()

if __name__ == '__main__':
    processManager()
