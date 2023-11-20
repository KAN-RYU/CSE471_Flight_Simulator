import numpy as np
import matplotlib.pyplot as plt
from time import time

"""
Ccodes below from 
https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html

"""

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency*res[0], frequency*res[1]))
        frequency *= 2
        amplitude *= persistence
    return noise

"""
End here
"""

def apply_gradient_map(noise: np.ndarray, rate=0.5) -> np.ndarray:
    x, y = np.meshgrid(np.linspace(-1, 1, noise.shape[0]), np.linspace(-1, 1, noise.shape[1]))
    d = np.sqrt(x**2 + y**2)
    mu = 0
    g = np.exp(-((d-mu)**2 / (2.0*rate**2)))
    return (noise + g)-0.5

def get_terrain_vertices_array(noise: np.ndarray) -> np.ndarray:
    size = noise.shape[0]
    center = size // 2
    x = np.linspace(-center, center-1, size, dtype='float32')
    x = np.hstack([x]*size)
    z = np.linspace(-center, center-1, size, dtype='float32')
    z = np.vstack([z.T]*size).flatten()
    y = noise.flatten()
    result = np.vstack([x, y, z]).flatten('F')
    return result
    

if __name__ == "__main__":
    np.random.seed(int(time()))
    size = 256
    r = 8
    noise = generate_fractal_noise_2d(shape=(size, size), res=(r, r), octaves=5, persistence=0.5)
    noise = apply_gradient_map(noise, rate=0.3)
    get_terrain_vertices_array(noise)
    plt.imshow(noise, cmap='terrain', vmin=-0.8, vmax=0.8)
    plt.colorbar()
    plt.show()
