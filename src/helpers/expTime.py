import numpy as np

def exp_time(rate, ri):
    return -(1 / rate) * np.log(1 - ri)