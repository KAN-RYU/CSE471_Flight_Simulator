from __future__ import annotations

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing import Callable
import numpy as np
from SGEngine.quaternion import *
from enum import Enum

class ComponentType(Enum):
    RIGIDBODY = 1
    CAMERA = 2
    SCRIPT = 3

class GameObject:
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        self.position = position
        self.rotation = Quaternion.from_euler_vec(rotation)
        self.scale = scale

        self.worldMat = np.identity(4)
        self.needUpdate = True

        self.parent: GameObject = None
        self.children: list[GameObject] = []
        self.components: list[Component] = []

        # Callbacks

        # Update Callbacks - Called every frame - input: (GameObject, dt)
        self.updateCallbacks: list[Callable[[GameObject, float], None]] = []
        # Keyboard Callbacks - Called when keyboard event occurs - input: (GameObject, key, x, y)
        self.keyboardCallbacks: list[Callable[[GameObject, int, int, int], None]] = []
        # KeyboardUp Callbacks - Called when keyboard up event occurs - input: (GameObject, key, x, y)
        self.keyboardUpCallbacks: list[Callable[[GameObject, int, int, int], None]] = []
        # Mouse Callbacks - Called when mouse event occurs - input: (GameObject, button, state, x, y)
        self.mouseCallbacks: list[Callable[[GameObject, int, int, int, int], None]] = []
        # Motion Callbacks - Called when motion event occurs - input: (GameObject, x, y)
        self.motionCallbacks: list[Callable[[GameObject, int, int], None]] = []
        # MouseMove Callbacks - Called when mouse move event occurs - input: (GameObject, x, y)
        self.mouseMoveCallbacks: list[Callable[[GameObject, int, int], None]] = []

    def getTranslationMat(self):
        return np.array([
            [1, 0, 0, self.position[0]],
            [0, 1, 0, self.position[1]],
            [0, 0, 1, self.position[2]],
            [0, 0, 0, 1               ]
        ])
    
    def getRotationMat(self):
        return self.rotation.to_rotation_matrix()
    
    def getScaleMat(self):
        return np.array([
            [self.scale[0], 0,             0,             0],
            [0,             self.scale[1], 0,             0],
            [0,             0,             self.scale[2], 0],
            [0,             0,             0,             1]
        ])
    
    def getLocalMat(self):
        return self.getTranslationMat() @ self.getRotationMat() @ self.getScaleMat()
    
    def updateWorldMat(self, parentUpdated=False):
        if self.needUpdate or parentUpdated:
            if self.parent is None:
                self.worldMat = self.getLocalMat()
            else:
                self.worldMat = self.parent.worldMat @ self.getLocalMat()

        for child in self.children:
            child.updateWorldMat(parentUpdated or self.needUpdate)

        self.needUpdate = False

    def getLocalVec(self, vec):
        return (self.worldMat @ np.append(vec, 0))[:3]

    def translate(self, translation):
        self.position = self.position + self.getLocalVec(translation)
        self.needUpdate = True

    def setPosition(self, position):
        self.position = position
        self.needUpdate = True

    def rotate(self, axis, angle):
        self.rotation = Quaternion.from_axis_angle(self.getLocalVec(axis), angle) * self.rotation
        self.needUpdate = True

    def setRotation(self, rotation):
        self.rotation = rotation
        self.needUpdate = True

    def lookat(self, target, up=np.array([0, 1, 0])):
        self.rotation = Quaternion.from_rotation_matrix(np.linalg.inv(np.eye(3) @ self.getLocalMat()[:3, :3])) * Quaternion.from_rotation_matrix(np.linalg.inv(np.eye(3) @ np.array([
            [1, 0, 0, target[0]],
            [0, 1, 0, target[1]],
            [0, 0, 1, target[2]],
            [0, 0, 0, 1]
        ])[:3, :3]))
        self.needUpdate = True

    def scale(self, scale):
        self.scale *= scale
        self.needUpdate = True

    def setScale(self, scale):
        self.scale = scale
        self.needUpdate = True

    def draw(self):
        self.drawSelf()
        self.drawChildren()
    
    def drawSelf(self):
        pass

    def drawChildren(self):
        for child in self.children:
            child.draw()

    def addChild(self, child):
        child.parent = self
        self.children.append(child)

    def removeChild(self, child):
        child.parent = None
        self.children.remove(child)

    def addComponent(self, component: Component):
        component.register(self)

    def getComponent(self, componentType: ComponentType):
        for component in self.components:
            if component.getType() == componentType:
                return component
        return None
    
    def getComponents(self, componentType: ComponentType):
        components = []
        for component in self.components:
            if component.getType() == componentType:
                components.append(component)
        return components
    
    def register(self, scene):
        self.scene = scene

    def init(self):
        for component in self.components:
            if component.getType() == ComponentType.SCRIPT:
                component.Start(self)

    def update(self, dt):
        for callback in self.updateCallbacks:
            callback(self, dt)
    
    def keyboard(self, key, x, y):
        for callback in self.keyboardCallbacks:
            callback(self, key, x, y)

    def keyboardUp(self, key, x, y):
        for callback in self.keyboardUpCallbacks:
            callback(self, key, x, y)

    def mouse(self, button, state, x, y):
        for callback in self.mouseCallbacks:
            callback(self, button, state, x, y)

    def motion(self, x, y):
        for callback in self.motionCallbacks:
            callback(self, x, y)

    def mouseMove(self, x, y):
        for callback in self.mouseMoveCallbacks:
            callback(self, x, y)

class Component:
    def __init__(self):
        pass
    
    def getType(self) -> ComponentType:
        raise NotImplementedError

    def register(self, gameObject: GameObject):
        self.object = gameObject
        gameObject.components.append(self)

class Cube(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidCube(1)
        glPopMatrix()
        glColor3f(1.0, 1.0, 1.0)

class Sphere(GameObject):
    def __init__(self, position, rotation, scale):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidSphere(1, 20, 20)
        glPopMatrix()

class Cylinder(GameObject):  
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidCylinder(1, 1, 20, 20)
        glPopMatrix()

class Cone(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidCone(1, 1, 20, 20)
        glPopMatrix()

class Torus(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidTorus(0.5, 1, 20, 20)
        glPopMatrix()

class Teapot(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        glutSolidTeapot(1)
        glPopMatrix()

class Plane(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)

    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)

        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-1, 0, -1)
        glVertex3f(-1, 0, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 0, -1)
        glEnd()

        glPopMatrix()
