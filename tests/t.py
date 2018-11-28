import threading
import time


def worker():
    """thread worker function"""
    print('Worker')
    time.sleep(1)
    print('Done')
    return


class Exiter(object):
    def __init__(self):
        self.a = 5.0
        print('I am alive')


exiter = Exiter()

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("main Exit")
