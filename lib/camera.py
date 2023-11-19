import numpy as np
from lib.gameobject import *

class Camera(Component):
    def __init__(self, fov=45, up=np.array([0, 1, 0]), near=0.1, far=100):
        self.up = up
        self.fov = fov
        self.near = near
        self.far = far

    def getType(self) -> ComponentType:
        return ComponentType.CAMERA
    
    def register(self, gameObject: GameObject):
        super().register(gameObject)

    def getViewMat(self) -> np.ndarray:
        """
        Returns the view matrix of the camera.
        """
        return np.linalg.inv(self.object.worldMat @ np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]))