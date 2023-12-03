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
        glTranslatef(-3, -1.5, 1)
        glRotatef(180, 0, 1, 0)
        glScale(0.5, 0.5, 0.5)
        self.obj.render()
        # glRotatef(-90, 1, 0, 0)
        # glRotatef(90, 0, 0, 1)
        # self.obj.render()