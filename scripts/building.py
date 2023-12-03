from SGEngine.gameobject import *
from SGEngine.rigidbody import RigidBody
from SGEngine.script import Script
from SGEngine.quaternion import *
from SGEngine.collision import *
import numpy as np
v = []
vn = []
adj_f = []
meshes = []

with open("models/building1.obj", 'r') as file:
    lines = file.readlines()

for line in lines:
    data = line.split()
    if data[0] == "v":
        v.append([float(i) for i in data[1:]])
    elif data[0] == "vt":
        vn.append([float(i) for i in data[1:]])
    elif data[0] == "f":
        adj_f.append([data[i].split('/') for i in range(1, len(data))])
for f in adj_f:
    vertices = np.array([v[int(f[i][0]) - 1] for i in range(len(f))]) * 10
    edge1 = vertices[1] - vertices[0]
    edge2 = vertices[2] - vertices[0]
    normal = np.cross(edge1, edge2)
    normal = normal / np.linalg.norm(normal) 
    mesh = Mesh(vertices, normal)
    meshes.append(mesh)

class Building(GameObject):
    def __init__(self,position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3), init_pos = np.array([0,-7,-200])):
        super().__init__(position, rotation, scale)
        self.meshes = meshes
        self.mat = self.getLocalMat().copy()
        self.init_pos = init_pos
        

    def drawSelf(self):
        glPushMatrix()
        glColor3f(1.,1.,1.)
        glMultMatrixf(self.mat.T)
        glBegin(GL_TRIANGLES)
        for mesh in self.meshes:
            normal = mesh.normal
            glNormal3f(*normal)
            for vertice in mesh.vertices:
                glVertex3f(*(vertice + self.init_pos))
        glEnd()
        glPopMatrix()
        

    def update(self, dt):
        pass