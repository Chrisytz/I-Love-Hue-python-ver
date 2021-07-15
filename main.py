from screen import run_all
from screen import play_sound
import multiprocessing
import time
from multiprocessing.pool import ThreadPool
import config

config.init()
mylist = [ False]

def manager():
    p3 = multiprocessing.Process(target=play_sound)
    p3.start()
    # p3.terminate()
    while(True):

        print(mylist[0])
        time.sleep(1)
        if mylist[0] == True:
            p3.terminate()

def music():
    p2 = multiprocessing.Process(target=play_sound)
    p2.start()
    while True:
        if config._finish:
            print("frick uuuu")
            break
        p2.join()
    print("terminated")
    p2.terminate()


if __name__ == '__main__':
    # pool = ThreadPool(processes=2)
    # pool.apply_async(run_all)
    # pool.apply_async(play_sound)
    # FINISH = True
    # pool.terminate()
    # pool.join()
    p1 = multiprocessing.Process(target=run_all, args=(mylist, ))
    p2 = multiprocessing.Process(target=manager)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
