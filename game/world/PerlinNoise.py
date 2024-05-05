import random
import math
import threading


class PerlinNoise(threading.Thread):
    def __call__(self, x, y): return int(sum(self.noise(x * s, y * s) * h for s, h in self.perlins) * self.avg)

    def __init__(self, seed=10000, mh=0):
        super().__init__()
        self.m = 65536
        p = list(range(self.m))
        random.seed(seed)
        random.shuffle(p)
        self.p = p + p
        p = self.perlins = tuple((1 / i, i) for i in (16, 20, 22, 31, 32, 64, 512) for j in range(2))
        self.pp = p
        self.avg = mh * len(p) / sum(f + i for f, i in p)

    def updateAvg(self, mh):
        self.avg = mh * len(self.pp) / sum(f + i for f, i in self.pp)

    def fade(self, t): return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b): return a + t * (b - a)

    def grad(self, hash, x, y, z):
        h = hash & 15
        u = y if h & 8 else x
        v = (x if h == 12 or h == 14 else z) if h & 12 else y
        return (u if h & 1 else -u) + (v if h & 2 else -v)

    def noise(self, x, y, z=0):
        p, fade, lerp, grad = self.p, self.fade, self.lerp, self.grad
        xf, yf, zf = math.floor(x), math.floor(y), math.floor(z)
        X, Y, Z = xf % self.m, yf % self.m, zf % self.m
        x -= xf
        y -= yf
        z -= zf
        u, v, w = fade(x), fade(y), fade(z)
        A = p[X] + Y
        AA = p[A] + Z
        AB = p[A + 1] + Z
        B = p[X + 1] + Y
        BA = p[B] + Z
        BB = p[B + 1] + Z
        return lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z), grad(p[BA], x - 1, y, z)),
                            lerp(u, grad(p[AB], x, y - 1, z), grad(p[BB], x - 1, y - 1, z))),
                    lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1), grad(p[BA + 1], x - 1, y, z - 1)),
                         lerp(u, grad(p[AB + 1], x, y - 1, z - 1), grad(p[BB + 1], x - 1, y - 1, z - 1))))


class NoiseGeneratorPerlin:  # Used in Normal Minecraft
    def __init__(self):
        self.permutations = [0] * 512
        self.xCoord_03 = random.random() * 256.0
        self.yCoord_03 = random.random() * 256.0
        self.zCoord_03 = random.random() * 256.0

        for j in range(256):
            self.permutations[j] = j

        for j in range(256):
            k = random.randint(j, 255)
            self.permutations[j], self.permutations[k] = self.permutations[k], self.permutations[j]
            self.permutations[j + 256] = self.permutations[j]

    def generate_noise(self, d, d1, d2):
        d3 = d + self.xCoord_03
        d4 = d1 + self.yCoord_03
        d5 = d2 + self.zCoord_03
        i = int(d3) & 255
        j = int(d4) & 255
        k = int(d5) & 255
        d3 -= int(d3)
        d4 -= int(d4)
        d5 -= int(d5)
        d6 = d3 * d3 * d3 * (d3 * (d3 * 6.0 - 15.0) + 10.0)
        d7 = d4 * d4 * d4 * (d4 * (d4 * 6.0 - 15.0) + 10.0)
        d8 = d5 * d5 * d5 * (d5 * (d5 * 6.0 - 15.0) + 10.0)
        l = self.permutations[i] + j
        i1 = self.permutations[l] + k
        j1 = self.permutations[l + 1] + k
        l1 = self.permutations[i + 1] + j
        i2 = self.permutations[l1] + k
        j2 = self.permutations[l1 + 1] + k
        return self.lerp(d8, self.lerp(d7, self.lerp(d6, self.grad(self.permutations[i1], d3, d4, d5),
                                                     self.grad(self.permutations[i2], d3 - 1.0, d4, d5)),
                                       self.lerp(d6, self.grad(self.permutations[j1], d3, d4 - 1.0, d5),
                                                 self.grad(self.permutations[j2], d3 - 1.0, d4 - 1.0, d5))),
                         self.lerp(d7, self.lerp(d6, self.grad(self.permutations[i1 + 1], d3, d4, d5 - 1.0),
                                                 self.grad(self.permutations[i2 + 1], d3 - 1.0, d4, d5 - 1.0)),
                                   self.lerp(d6, self.grad(self.permutations[j1 + 1], d3, d4 - 1.0, d5 - 1.0),
                                             self.grad(self.permutations[j2 + 1], d3 - 1.0, d4 - 1.0, d5 - 1.0))))

    def lerp(self, d, d1, d2):
        return d1 + d * (d2 - d1)

    def func_4110_a(self, i, d, d1):
        j = i & 15
        d2 = (1 - ((j & 8) >> 3)) * d
        d3 = d1 if j >= 4 else 0.0
        return (-d2 if j & 1 else d2) + (-d3 if j & 2 else d3)

    def grad(self, i, d, d1, d2):
        j = i & 15
        d3 = d1 if j >= 8 else d
        d4 = d2 if j >= 4 else (d1 if j in (12, 14) else d)
        return (-d3 if j & 1 else d3) + (-d4 if j & 2 else d4)

    def func_801_a(self, d, d1):
        return self.generate_noise(d, d1, 0.0)

    def func_805_a(self, ad, d, d1, d2, i, j, k, d3, d4, d5, d6):
        if j == 1:
            for i4 in range(i):
                d15 = (d + i4) * d3 + self.xCoord_03
                j4 = int(d15)
                if d15 < j4:
                    j4 -= 1
                k4 = j4 & 255
                d15 -= j4
                d18 = d15 * d15 * d15 * (d15 * (d15 * 6.0 - 15.0) + 10.0)
                for l4 in range(k):
                    d20 = (d2 + l4) * d5 + self.zCoord_03
                    j5 = int(d20)
                    if d20 < j5:
                        j5 -= 1
                    i6 = j5 & 255
                    d20 -= j5
                    d22 = d20 * d20 * d20 * (d20 * (d20 * 6.0 - 15.0) + 10.0)
                    l = self.permutations[k4] + 0
                    j1 = self.permutations[l] + i6
                    k1 = self.permutations[k4 + 1] + 0
                    k6 = self.permutations[k1] + i6
                    d9 = self.lerp(d18, self.func_4110_a(self.permutations[j1], d15, d20),
                                   self.grad(self.permutations[k6], d15 - 1.0, 0.0, d20))
                    d11 = self.lerp(d18, self.grad(self.permutations[j1 + 1], d15, 0.0, d20 - 1.0),
                                    self.grad(self.permutations[k6 + 1], d15 - 1.0, 0.0, d20 - 1.0))
                    d26 = self.lerp(d22, d9, d11)
                    ad[i4] += d26 / d6
        else:
            i1 = 0
            d7 = 1.0 / d6
            i2 = -1
            for l4 in range(i):
                d20 = (d + l4) * d3 + self.xCoord_03
                j5 = int(d20)
                if d20 < j5:
                    j5 -= 1
                i6 = j5 & 255
                d20 -= j5
                d22 = d20 * d20 * d20 * (d20 * (d20 * 6.0 - 15.0) + 10.0)
                for l in range(k):
                    d24 = (d2 + l) * d5 + self.zCoord_03
                    k6 = int(d24)
                    if d24 < k6:
                        k6 -= 1
                    l6 = k6 & 255
                    d24 -= k6
                    d25 = d24 * d24 * d24 * (d24 * (d24 * 6.0 - 15.0) + 10.0)
                    for i7 in range(j):
                        d26 = (d1 + i7) * d4 + self.yCoord_03
                        j7 = int(d26)
                        if d26 < j7:
                            j7 -= 1
                        k7 = j7 & 255
                        d26 -= j7
                        d27 = d26 * d26 * d26 * (d26 * (d26 * 6.0 - 15.0) + 10.0)
                        if i7 == 0 or k7 != i2:
                            i2 = k7
                            j2 = self.permutations[i6] + k7
                            k2 = self.permutations[j2] + l6
                            l2 = self.permutations[j2 + 1] + l6
                            i3 = self.permutations[i6 + 1] + k7
                            k3 = self.permutations[i3] + l6
                            l3 = self.permutations[i3 + 1] + l6
                            d13 = self.lerp(d22, self.grad(self.permutations[k2], d20, d26, d24),
                                            self.grad(self.permutations[k3], d20 - 1.0, d26, d24))
                            d15 = self.lerp(d22, self.grad(self.permutations[l2], d20, d26 - 1.0, d24),
                                            self.grad(self.permutations[l3], d20 - 1.0, d26 - 1.0, d24))
                            d16 = self.lerp(d22, self.grad(self.permutations[k2 + 1], d20, d26, d24 - 1.0),
                                            self.grad(self.permutations[k3 + 1], d20 - 1.0, d26, d24 - 1.0))
                            d18 = self.lerp(d22, self.grad(self.permutations[l2 + 1], d20, d26 - 1.0, d24 - 1.0),
                                            self.grad(self.permutations[l3 + 1], d20 - 1.0, d26 - 1.0, d24 - 1.0))
                        d28 = self.lerp(d27, d13, d15)
                        d29 = self.lerp(d27, d16, d18)
                        d30 = self.lerp(d25, d28, d29)
                        ad[i1] += d30 / d7
                        i1 += 1

