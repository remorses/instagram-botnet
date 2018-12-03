

def start(threads):
    [thread.start() for thread in threads]
    return threads


def wait(threads):
    [thread.join() for thread in threads]
    return threads


def reset():
    return []
