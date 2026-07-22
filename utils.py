import time

start = 0

def start_timer():
    global start
    start = time.time()

def end_timer():
    return round((time.time() - start) * 1000, 2)