from threading import Lock
mylock = Lock()
p = print

def safe_print(*a, **b):
	with mylock:
		p(*a, **b)
