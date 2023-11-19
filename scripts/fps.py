from OpenGL.GLUT import *
import numpy as np
from lib.script import *
from lib.quaternion import *

class FPSController(Script):
    def __init__(self):
        super().__init__()
        self.speed = 10
        self.sensitivity = 0.01
        self.hInput = 0
        self.vInput = 0
        self.prev_x = None
        self.prev_y = None

    def Start(self, gameObject: GameObject):
        glutSetCursor(GLUT_CURSOR_NONE)

    def Update(self, gameObject: GameObject, dt: float):
        dir = np.array([float(self.hInput), 0, float(self.vInput)], dtype=np.float64) * dt * self.speed
        gameObject.translate(dir)

    def Keyboard(self, gameObject: GameObject, key: int, x: int, y: int):
        if key == b'w':
            self.vInput = -1
        if key == b's':
            self.vInput = 1
        if key == b'a':
            self.hInput = -1
        if key == b'd':
            self.hInput = 1

    def KeyboardUp(self, gameObject: GameObject, key: int, x: int, y: int):
        if key == b'w' or key == b's':
            self.vInput = 0
        if key == b'a' or key == b'd':
            self.hInput = 0

    def MouseMove(self, gameObject: GameObject, x: int, y: int):
        if self.prev_x is None:
            self.prev_x = x
            self.prev_y = y
        dx = x - self.prev_x
        dy = self.prev_y - y
        self.prev_x = x
        self.prev_y = y
        
        # camera rotation
        r = Quaternion.from_axis_angle(np.array([0, 1, 0]), -dx * self.sensitivity) * gameObject.rotation
        r = r * Quaternion.from_axis_angle(np.array([1, 0, 0]), dy * self.sensitivity)
        r.normalize()
        
        gameObject.setRotation(r)

        glutPostRedisplay()

        # warp cursor
        if x < 100 or x > self.object.scene.width - 100 or y < 100 or y > self.object.scene.height - 100:
            glutWarpPointer(self.object.scene.width // 2, self.object.scene.height // 2)
            self.prev_x = self.object.scene.width // 2
            self.prev_y = self.object.scene.height // 2