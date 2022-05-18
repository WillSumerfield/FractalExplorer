"""A list of fractal functions"""

def mandelbrot(c, iterations=80):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iterations:
        z = z*z + c
        n += 1
    return n
