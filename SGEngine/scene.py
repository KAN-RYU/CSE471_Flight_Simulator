from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from SGEngine.gameobject import *
from SGEngine.camera import Camera
from SGEngine.model import Model
from SGEngine.skybox import Skybox
import numpy as np
import time as t

class Scene:
    time = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.skybox = None

        self.prev_time = 0

        self.objects: list[GameObject] = []

    def setCamera(self, camera_obj:GameObject):
        self.camera_obj = camera_obj
        camera = camera_obj.getComponent(ComponentType.CAMERA) if camera_obj is not None else None
        if camera is not None and isinstance(camera, Camera):
            self.camera = camera
        else:
            self.camera = None
    
    def light(self):
        """
        Light used in the scene.
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # feel free to adjust light colors
        lightAmbient = [0.5, 0.5, 0.5, 1.0]
        lightDiffuse = [0.5, 0.5, 0.5, 1.0]
        lightSpecular = [0.5, 0.5, 0.5, 1.0]
        lightPosition = [1, 1, -1, 0]  # vector: point at infinity
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)

    def display(self):
        """
        Display callback function for the main window.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        self.drawScene()

        glutSwapBuffers()

    # Assignment 2. Task 3 - implement resize function
    def reshape(self, w, h):
        """
        Reshape callback function.\n
        Does notihing as of now.
        """
        # print(f"reshape to width: {w}, height: {h}")

        # update variables
        self.width = w
        self.height = h

        # resize the main window
        glViewport(0, 0, w, h)
        glutReshapeWindow(w, h)


    def mouse(self, button, state, x, y):
        """
        Mouse callback function.
        """
        # print(f"Display #{glutGetWindow()} mouse event: button={button}, state={state}, x={x}, y={y}")

        for obj in self.objects:
            obj.mouse(button, state, x, y)


    def motion(self, x, y):
        """
        Motion callback function.
        """
        # print(f"Display #{glutGetWindow()} motion event: x={x}, y={y}")

        for obj in self.objects:
            obj.motion(x, y)


    def mouseMove(self, x, y):
        """
        Mouse move callback function.
        """
        # print(f"Display #{glutGetWindow()} mouse move event: x={x}, y={y}")

        for obj in self.objects:
            obj.mouseMove(x, y)


    def keyboard(self, key, x, y):
        """
        Keyboard callback function.
        """
        # print(f"Display #{glutGetWindow()} keyboard event: key={key}, x={x}, y={y}")
        if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
            print("shift pressed")
        if glutGetModifiers() & GLUT_ACTIVE_ALT:
            print("alt pressed")
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")

        for obj in self.objects:
            obj.keyboard(key, x, y)
        

    def keyboardup(self, key, x, y):
        """
        Keyboard up callback function.
        """
        # print(f"Display #{glutGetWindow()} keyboard up event: key={key}, x={x}, y={y}")

        for obj in self.objects:
            obj.keyboardUp(key, x, y)


    def special(self, key, x, y):
        """
        Special key callback function.
        """
        # print(f"Display #{glutGetWindow()} special key event: key={key}, x={x}, y={y}")    


    def update(self, dt):
        """
        Update callback function.
        """
        for obj in self.objects:
            obj.update(dt)

        Scene.time += dt

    def timer(self, value):
        current_time = t.time()
        if self.prev_time != 0:
            dt = current_time - self.prev_time

            self.update(1/60)

            glutPostRedisplay()

        self.prev_time = current_time
        glutTimerFunc(1000//60, self.timer, 0)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(0, 0)
        self.mainWindow = glutCreateWindow(b"Flight Simulator")
        glutSetWindow(self.mainWindow)

        # load skybox
        self.skybox = Skybox(self)
        self.skybox.loadTextures()
        self.skybox.draw()
        # initialize
        for obj in self.objects:
            obj.init()

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutPassiveMotionFunc(self.mouseMove)
        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc(self.keyboardup)
        glutSpecialFunc(self.special)

        self.light()
        glutSetWindow(self.mainWindow)
        self.timer(0)
        glutMainLoop()

    def drawScene(self):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.camera_obj is not None:
            gluPerspective(self.camera.fov, self.width / self.height, self.camera.near, self.camera.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.camera_obj is not None:
            glMultMatrixf(self.camera.getViewMat().T)
        
        if self.skybox is not None:
            self.skybox.draw()

        for obj in self.objects:
            obj.updateWorldMat()
            obj.draw()

        self.drawAxes()

    def drawAxes(self):
        glPushMatrix()
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0.1, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0.1, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 0.1)
        glColor3f(1, 1, 1)
        glEnd()
        glPopMatrix()

    def addObject(self, obj: GameObject):
        obj.register(self)
        self.objects.append(obj)