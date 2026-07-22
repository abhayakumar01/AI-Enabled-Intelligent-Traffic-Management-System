import numpy as np

history = []

def update(value):
    history.append(value)
    if len(history) > 10:
        history.pop(0)

def predict():
    if len(history) < 3:
        return history[-1] if history else 0

    weights = np.linspace(1, 2, len(history))
    return int(np.average(history, weights=weights)) 