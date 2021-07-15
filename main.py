from screen import run_all
from screen import play_sound
import multiprocessing
import time
import config
from multiprocessing.pool import ThreadPool


def manager():
    p3 = multiprocessing.Process(target=play_sound)
    p3.start()
    # p3.terminate()
    while(True):
        print(config._finish)
        time.sleep(1)
        if config._finish == True:
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
    p1 = multiprocessing.Process(target=run_all)
    p2 = multiprocessing.Process(target=manager)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
