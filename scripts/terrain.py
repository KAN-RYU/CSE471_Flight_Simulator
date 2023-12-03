import numpy as np
import matplotlib.pyplot as plt
from time import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from SGEngine.gameobject import GameObject
from SGEngine.quaternion import np
from scripts.terrain_generator import *

from PIL import Image

rockTex = Image.open('./textures/IMGP5525_seamless.jpg').convert("RGB")
dirtTex = Image.open('./textures/IMGP5487_seamless.jpg').convert("RGB")
grassTex = Image.open('./textures/tilable-IMG_0044-verydark.png').convert("RGB")
snowTex = Image.open('./textures/water.png').convert("RGB")

rockTexArray = np.array(rockTex)
dirtTexArray = np.array(dirtTex)
grassTexArray = np.array(grassTex)
snowTexArray = np.array(snowTex)

class Terrain(GameObject):
    size = 10
    height = 5
    interp: RectBivariateSpline
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3), resolution=128, divide=8, size=10, height=5):
        super().__init__(position, rotation, scale)
        np.random.seed(int(time()))
        Terrain.size = size
        Terrain.height = height
        r = divide
        noise = generate_fractal_noise_2d(shape=(resolution, resolution), res=(r, r), octaves=5, persistence=0.5)
        noise = apply_gradient_map(noise, rate=0.3)
        self.vertices = get_terrain_vertices_array(noise, height) * size
        self.normals = get_terrain_normal_array(self.vertices)
        self.indices = get_tri_indices_array(resolution)
        self.colors = get_color_array(noise)
        lerpCondition = np.array([0.2, 0.6, 1.0, 1.6])
        self.tex, Terrain.interp = get_texture_array_interp(noise, [rockTexArray, dirtTexArray, grassTexArray, snowTexArray], lerpCon=lerpCondition)
        # Image.fromarray((self.tex*255).astype(np.uint8), mode="RGB").show()
        x, y = np.meshgrid(np.linspace(0, 1, resolution), np.linspace(0, 1, resolution))
        self.texCoord = np.stack([x,y], axis=2).flatten()
        print(self.vertices[:3])
        
        self.texid =  None
        
        
    
    def drawSelf(self):
        if not self.texid:
            self.texid = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1024, 1024, 0, GL_RGB, GL_FLOAT, self.tex)
        
        glColor3f(1.0, 1.0, 1.0)
        # glShadeModel(GL_FLAT)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texid)
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        # glEnableClientState(GL_COLOR_ARRAY)
        # glColorPointer(3, GL_FLOAT, 0, self.colors)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texCoord)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 0, self.normals)        
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)   
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
        
        floor = [[100, 0.0, 100],
                 [-100, 0.0, 100],
                 [-100, 0.0, -100],
                 [100, 0.0, -100],]
        floor = np.array(floor)
        floor = floor * Terrain.size
        glPushMatrix()
        glColor3f(0.6, 0.5, 0.2)
        glMultMatrixd(self.worldMat.T)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)
        for vertice in floor:
            glVertex3f(*(vertice))
        glEnd()
        glPopMatrix()
        
        water = [[100, 0.5*Terrain.height, 100],
                 [-100, 0.5*Terrain.height, 100],
                 [-100, 0.5*Terrain.height, -100],
                 [100, 0.5*Terrain.height, -100],]
        water = np.array(water)
        water = water * Terrain.size
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPushMatrix()
        glColor4f(0.0, 0.2, 1.0, 0.6)
        glMultMatrixd(self.worldMat.T)
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)
        for vertice in water:
            glVertex3f(*(vertice))
        glEnd()
        glPopMatrix()
        glDisable(GL_BLEND)
        

