from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from SGEngine.objloader import OBJ

class Model:
    def __init__(self, path):
        self.loadModel(path)

    def loadModel(self, path):
        self.obj = OBJ(path)

    def draw(self):
        glScale(0.5, 0.5, 0.5)
        glTranslatef(-5.5, -3, 2)
        glRotatef(180, 0, 1, 0)
        self.obj.render()