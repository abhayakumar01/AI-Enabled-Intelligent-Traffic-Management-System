import random

def get_signal_time(score):
    if score < 10:
        t = 20
    elif score < 30:
        t = 40
    else:
        t = 60

    t += random.choice([-5, 0, 5])

    return max(15, min(70, t))