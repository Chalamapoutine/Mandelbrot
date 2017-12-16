from time import time
from numba import jit


def dictiobrot_equalizer(dictiobrot, max_it, exposant=4):

    t = time()
    print("> equalisating")
    res = len(dictiobrot)
    cdf = cumulative_distibutive_function(dictiobrot, max_it, res)

    for a in dictiobrot:
        dictiobrot[a] = (cdf[dictiobrot[a]] ** exposant) * max_it
    delta_t = time() - t
    print(">/equalised in {}sec".format(delta_t))
    return dictiobrot


def cumulative_distibutive_function(sortobrot, max_it, resolution):

    cdf = [0]*(max_it + 1)

    for e, level in enumerate(sortobrot):  # Compute the histogram

        if level == -1:
            del sortobrot[e]

        else:
            cdf[int(level)] += 1

    for i in range(len(cdf)):  # Sum the histogram.
        cdf[i] /= len(sortobrot)  # If a ZeroDivision error is raised, the picture is full black.

        if i != 0:
            cdf[i] += cdf[i-1]

    return cdf
