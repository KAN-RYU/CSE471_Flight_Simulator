from SGEngine.script import *
# from SGEngine.quaternion import *
import numpy as np
from SGEngine.quaternion import Quaternion

class CameraController(Script):
    def __init__(self, target: GameObject):
        super().__init__()
        self.target = target
        self.alpha = 0.5
        self.rotalpha = 0.1
        self.rotoffset = np.array([-np.pi / 8, 0, 0])
        self.offset = np.array([0, 2, 6])

    def Update(self, obj: GameObject, dt: float):
        obj.setPosition(self.target.position + self.target.getLocalVec(self.offset))
        rot = self.target.rotation * Quaternion.from_euler(*self.rotoffset)
        rot.normalize()
        obj.setRotation(rot)