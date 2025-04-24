import random

def addnoise(val):

    def add_noise(mean, std_dev, val):

        noise = random.gauss(mean, std_dev)
        result = val + noise
        return result


    return add_noise(0,2,val)


addnoise.registered = True
