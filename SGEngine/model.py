from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from SGEngine.objloader import OBJ
import ctypes
import pywavefront

class Model:
    def __init__(self, path):
        self.loadModel(path)

    def loadModel(self, path):
        self.obj = OBJ(path)

    def draw(self):
        glRotatef(-90, 1, 0, 0)
        glRotatef(90, 0, 0, 1)
        self.obj.render()