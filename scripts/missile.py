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
max_x, max_y, max_z = -100, -100, -100
min_x, min_y, min_z = 100, 100, 100

with open("models/missile.obj", 'r') as file:
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
    vertices = np.array([v[int(f[i][0]) - 1] for i in range(len(f))]) * 0.1
    edge1 = vertices[1] - vertices[0]
    edge2 = vertices[2] - vertices[0]
    normal = np.cross(edge1, edge2)
    norm = np.linalg.norm(normal) 
    if norm < 0.0000001: continue
    normal = normal / norm
    mesh = Mesh(vertices, normal)
    meshes.append(mesh)

class Missile(GameObject):
    def __init__(self, velocity, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)
        self.meshes = meshes
        self.mat = self.getRotationMat().copy()
        self.vel = velocity.copy()
        self.pos = np.zeros((3,))
        self.init_pos = position.copy()

        

    def drawSelf(self):
        glPushMatrix()
        glColor3f(0.62, 0.165, 0)
        glMultMatrixf(np.identity(4))
        glBegin(GL_POLYGON)
        for mesh in self.meshes:
            normal = mesh.normal
            glNormal3f(*normal)
            for vertice in mesh.vertices:
                vertice = self.mat[:3,:3]@np.array(vertice)
                glVertex3f(*(vertice + self.pos + self.init_pos))
        glEnd()
        glPopMatrix()
        

    def update(self, dt):
        self.pos += self.vel * dt * 5
