from psutil import net_io_counters
from threading import Thread
import time
from .safe_print import safe_print

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


class Network_logger(Thread):
    def __init__(self):
        super().__init__()
        self.elapsed_minutes = 0
        self.recv = 0
        self.sent = 0

    def run(self):
        try:
            while True:
                net_io_counters.cache_clear()
                net = net_io_counters(nowrap=True)
                self.recv = net.bytes_recv
                self.sent =  net.bytes_recv
                safe_print('[after {} min received {} and sent {}]'.format(self.elapsed_minutes, bytes2human(self.recv), bytes2human(self.sent)))
                time.sleep(60)
                self.elapsed_minutes += 1
        except KeyboardInterrupt:
            raise
