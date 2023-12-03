from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
    
def intersect(aabb1, aabb2, offset):
    for i in range(3):  
        if aabb1[1][i] + offset[i] < aabb2[0][i] or aabb1[0][i] + offset[i] > aabb2[1][i]:
            return False 
    return True

def collide(airplane, terrain, offset):
    if intersect(airplane.aabb, terrain.aabb, offset): 
        if airplane.right is None and terrain.right is None:  
            return True  
        elif airplane.right is None: 
            return collide(airplane, terrain.left, offset) or collide(airplane, terrain.right), offset
        elif terrain.right is None:  
            return collide(airplane.left, terrain, offset) or collide(airplane.right, terrain, offset)
        else:
            return collide(airplane.left, terrain.left, offset) or \
                   collide(airplane.left, terrain.right, offset) or \
                   collide(airplane.right, terrain.left, offset) or \
                   collide(airplane.right, terrain.right, offset)
    else:
        return False
    
def intersect_missile_aabb(missile, aabb, offset):
    for i in range(3):  
        if missile[i] < aabb[0][i] + offset[i] or missile[i] > aabb[1][i] + offset[i]:
            return False 
    return True

def collide_missile(missile, building, offset):
    if intersect_missile_aabb(missile, building.aabb, offset): 
        if len(building.meshes) < 100:  
            return True  
        else: 
            return collide_missile(missile, building.left, offset) or collide_missile(missile, building.right, offset)
    else:
        return False

    
class BVnode:
    def __init__(self, meshes):
        self.meshes = meshes
        self.aabb = self.calculate_aabb()
        if len(meshes) > 1:
            meshes.sort(key=lambda x: x.aabb[0][0])
            mid = len(meshes) // 2
            self.left = BVnode(meshes[:mid])
            self.right = BVnode(meshes[mid:])
        else:
            self.left = meshes[0]
            self.right = None

    def calculate_aabb(self):
        min_values = np.min([mesh.aabb[0] for mesh in self.meshes], axis=0)
        max_values = np.max([mesh.aabb[1] for mesh in self.meshes], axis=0)
        return min_values, max_values
    
    def draw(self):
        vertices = [
        [self.aabb[0][0], self.aabb[0][1], self.aabb[0][2]],
        [self.aabb[1][0], self.aabb[0][1], self.aabb[0][2]],
        [self.aabb[1][0], self.aabb[1][1], self.aabb[0][2]],
        [self.aabb[0][0], self.aabb[1][1], self.aabb[0][2]],
        [self.aabb[0][0], self.aabb[0][1], self.aabb[1][2]],
        [self.aabb[1][0], self.aabb[0][1], self.aabb[1][2]],
        [self.aabb[1][0], self.aabb[1][1], self.aabb[1][2]],
        [self.aabb[0][0], self.aabb[1][1], self.aabb[1][2]]
        ]

        lines = [
        (vertices[0], vertices[1]), (vertices[1], vertices[2]), (vertices[2], vertices[3]), (vertices[3], vertices[0]),
        (vertices[4], vertices[5]), (vertices[5], vertices[6]), (vertices[6], vertices[7]), (vertices[7], vertices[4]),
        (vertices[0], vertices[4]), (vertices[1], vertices[5]), (vertices[2], vertices[6]), (vertices[3], vertices[7])
        ]
        
        glLineWidth(.02)
        glBegin(GL_LINES)
        glColor3f(0,1,0)
        for line in lines:
            glVertex3fv(line[0])
            glVertex3fv(line[1])
        glColor3f(1,1,1)
        glEnd()
        if self.left:
            self.left.draw()
        if self.right:
            self.right.draw()
        
    
class Mesh:
    def __init__(self, vertices, normal):
        self.vertices = vertices
        self.normal = normal
        self.aabb = (np.min(vertices, axis = 0), np.max(vertices, axis = 0))

    
    def draw(self):
        vertices = [
        [self.aabb[0][0], self.aabb[0][1], self.aabb[0][2]],
        [self.aabb[1][0], self.aabb[0][1], self.aabb[0][2]],
        [self.aabb[1][0], self.aabb[1][1], self.aabb[0][2]],
        [self.aabb[0][0], self.aabb[1][1], self.aabb[0][2]],
        [self.aabb[0][0], self.aabb[0][1], self.aabb[1][2]],
        [self.aabb[1][0], self.aabb[0][1], self.aabb[1][2]],
        [self.aabb[1][0], self.aabb[1][1], self.aabb[1][2]],
        [self.aabb[0][0], self.aabb[1][1], self.aabb[1][2]]
        ]
        lines = [
        (vertices[0], vertices[1]), (vertices[1], vertices[2]), (vertices[2], vertices[3]), (vertices[3], vertices[0]),
        (vertices[4], vertices[5]), (vertices[5], vertices[6]), (vertices[6], vertices[7]), (vertices[7], vertices[4]),
        (vertices[0], vertices[4]), (vertices[1], vertices[5]), (vertices[2], vertices[6]), (vertices[3], vertices[7])
        ]

        glBegin(GL_LINES)
        glColor3f(0,1,0)
        for line in lines:
            glVertex3fv(line[0])
            glVertex3fv(line[1])
        glColor3f(1,1,1)
        glEnd()

