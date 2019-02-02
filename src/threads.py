from threading import _newname, current_thread, Event, _sys, _dangling, Thread


def start(threads):
    [thread.setDaemon(True) for thread in threads]
    [thread.start() for thread in threads]
    return threads


def wait(threads):
    [thread.join() for thread in threads]
    return threads


def reset():
    return []


def custom_init(self, group=None, target=None, name=None,
                args=(), kwargs=None, *, daemon=None):

    self._data = {}

    assert group is None, "group argument must be None for now"
    if kwargs is None:
        kwargs = {}
    self._target = target
    self._name = str(name or _newname())
    self._args = args
    self._kwargs = kwargs
    if daemon is not None:
        self._daemonic = daemon
    else:
        self._daemonic = current_thread().daemon
    self._ident = None
    self._tstate_lock = None
    self._started = Event()
    self._is_stopped = False
    self._initialized = True
    self._stderr = _sys.stderr
    _dangling.add(self)


def set_data(self, value):
    self._data = value


def get_data(self):
    return self._data


Thread.__init__ = custom_init
Thread.set_data = set_data
Thread.get_data = get_data
