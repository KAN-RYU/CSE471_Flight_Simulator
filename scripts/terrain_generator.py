from typing import List
import numpy as np
from time import time
if __name__ == "__main__":
    import utils
else:
    from . import utils
from tqdm import tqdm
from scipy.interpolate import RectBivariateSpline

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
    amplitude = 0.5
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency*res[0], frequency*res[1]))
        frequency *= 2
        amplitude *= persistence
    return noise

"""
End here
"""

def apply_gradient_map(noise: np.ndarray, rate=0.5) -> np.ndarray:
    """
    Applying Gaussian Gradient map
    """
    x, y = np.meshgrid(np.linspace(-1, 1, noise.shape[0]), np.linspace(-1, 1, noise.shape[1]))
    d = np.sqrt(x**2 + y**2)
    mu = 0.1
    g = np.exp(-((d-mu)**2 / (2.0*rate**2)))
    # h = np.multiply(noise, g)
    h = noise + g
    # return g
    h = h - np.min(h)
    h[0] = np.zeros(noise.shape[0])
    h[-1] = np.zeros(noise.shape[0])
    h[:,0] = np.zeros(noise.shape[0])
    h[:,-1] = np.zeros(noise.shape[0])
    return h

def get_terrain_vertices_array(noise: np.ndarray, height: float) -> np.ndarray:
    size = noise.shape[0]
    center = size // 2
    x = np.linspace(-center, center-1, size, dtype='float32')
    x = np.hstack([x]*size)
    z = np.linspace(-center, center-1, size, dtype='float32')
    z = np.hstack([np.reshape(z, (-1, 1))]*size).flatten()
    y = noise.flatten()
    y = y * height
    result = np.vstack([x, y, z]).flatten('F')
    return result

def get_terrain_normal_array(vertices: np.ndarray) -> np.ndarray:
    result = np.zeros(vertices.shape, dtype='float32')
    size = int(np.sqrt(vertices.shape[0]/3))
    n = (size-1)
    for i in tqdm(range(n)):
        for j in range(n):
            id = i*size+j
            v1 = np.array([vertices[(id)*3], vertices[(id)*3+1], vertices[(id)*3+2]])
            v2 = np.array([vertices[(id+size)*3], vertices[(id+size)*3+1], vertices[(id+size)*3+2]])
            v3 = np.array([vertices[(id+1)*3], vertices[(id+1)*3+1], vertices[(id+1)*3+2]])
            u = v2-v1
            v = v3-v1
            norm = np.cross(u, v)
            norm = norm / np.linalg.norm(norm)
            result[id*3] = norm[0]
            result[id*3+1] = norm[1]
            result[id*3+2] = norm[2]
    return result
    

def get_tri_indices_array(size=256) -> np.ndarray:
    result = np.array([],dtype='uint')
    n = (size-1)
    for i in tqdm(range(n)):
        for j in range(n):
            result = np.hstack([result, [(i*size+j), (i*size+j+size), (i*size+j+1), (i*size+j+1), (i*size+j+size), (i*size+j+size+1)]])
    return result

def get_color_array(noise: np.ndarray) -> np.ndarray:
    result = np.array([], dtype='float32')
    startColor = np.array([1.0, 0.5, 0.0])
    endColor = np.array([0.0, 1.0, 1.0])
    for y in tqdm(noise.flatten()):
        result = np.hstack([result, utils.vector_lerp(startColor, endColor, y)])
    return result

def get_texture_array(noise: np.ndarray, texs: List[np.ndarray], lerpCon: List[float]) -> np.ndarray:
    result = np.zeros((1024,1024,3), dtype='float32')
    interpolate_spline = RectBivariateSpline(np.linspace(0, 10, noise.shape[0]), np.linspace(0, 10, noise.shape[1]), noise)
    
    new_z = interpolate_spline(np.linspace(0, 10, 1024), np.linspace(0, 10, 1024))
    for i in range(len(lerpCon)):
        # upper
        l1 = new_z - lerpCon[i]
        l1 = np.clip(l1, a_min=0.0, a_max=2.0)
        l1 = l1 / (lerpCon[i+1]-lerpCon[i] if i != 3 else lerpCon[i])
        
        # lower
        l2 = new_z - lerpCon[i]
        l2 = np.clip(l2, a_min=-2.0, a_max=0.0)
        l2 = l2 / (lerpCon[i] - lerpCon[i-1] if i != 0 else lerpCon[i])
        l3 = np.clip(-np.absolute(l1 + l2)+1, a_min=0.0, a_max=1.0)
        
        l4 = np.stack([l3, l3, l3], axis=2)
        result += np.multiply(texs[i], l4)
    return result / 255
    
    

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    np.random.seed(int(time()))
    size = 128
    r = 8
    noise = generate_fractal_noise_2d(shape=(size, size), res=(r, r), octaves=5, persistence=0.5)
    noise = apply_gradient_map(noise, rate=0.4)
    # get_terrain_vertices_array(noise, 5)
    plt.imshow(noise, cmap='terrain', vmin=0.5, vmax=1.8)
    # plt.imshow(noise, cmap='terrain')
    plt.colorbar()
    plt.show()