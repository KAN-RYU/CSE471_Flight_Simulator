from SGEngine.gameobject import GameObject
from SGEngine.script import *
# from SGEngine.quaternion import *
import numpy as np
from SGEngine.quaternion import Quaternion

class CameraController(Script):
    def __init__(self, target: GameObject):
        super().__init__()
        self.target = target
        self.viewIndex = 0
        self.rotoffsets = np.array([[-np.pi / 8, 0, 0], [-np.pi / 8, np.pi, 0], [0, 0, 0]])
        self.offsets = np.array([[0, 2, 6], [0, 2, -8], [0, 0, -6]])

    def Update(self, obj: GameObject, dt: float):
        curOffset = self.offsets[self.viewIndex]
        curRotoffset = self.rotoffsets[self.viewIndex]
        obj.setPosition(self.target.position + self.target.getLocalVec(curOffset))
        rot = self.target.rotation * Quaternion.from_euler(*curRotoffset)
        rot.normalize()
        obj.setRotation(rot)

    def Keyboard(self, gameObject: GameObject, key: int, x: int, y: int):
        if key == b'v':
            self.nextView()

    def nextView(self):
        self.viewIndex = (self.viewIndex + 1) % len(self.offsets)