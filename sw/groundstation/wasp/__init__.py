import random, time, math

class NoisySine:
    def __init__(self, freq=1.0, amplitude=50.0, value_type=float, positive=True, noise_pct=10):
        self.t = time.time()
        self.dt = 0.0

        self.freq = freq
        self.amp = amplitude
        self.type = value_type

        #add 1 to sine to keep +ve
        if positive:
            self.offset = 1.0
        else:
            self.offset = 0.0

        #the noise is x percent of the amplitude
        n = (noise_pct/100.0) * self.amp
        self.n1 = self.amp - n
        self.n2 = self.amp + n
        

    def value(self):
        t = time.time()
        self.dt += (self.freq * (t - self.t))
        self.t = t

        val = (self.offset * math.sin(self.dt)) * self.amp
        noise = random.randrange(self.n1, self.n2, int=self.type)
        return self.type(noise + val)
