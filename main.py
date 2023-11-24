from SGEngine.scene import Scene
from SGEngine.gameobject import *
from SGEngine.camera import Camera
from SGEngine.rigidbody import RigidBody
from SGEngine.quaternion import *
from SGEngine.skybox import Skybox
from scripts.fps import FPSController
from scripts.airplane import AirplaneController
from scripts.terrain import Terrain
from scripts.camera import CameraController
from SGEngine.airplane import Airplane
import numpy as np
import pywavefront

if __name__ == "__main__":
    mainScene = Scene(1280, 720)
    airplane = Airplane(position=np.array([0.0, 100.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]))

    camera_obj = GameObject(position=np.array([0, 2, 6]), rotation=np.array([-np.pi/8, 0, 0]))
    camera_obj.addComponent(Camera(far = 4096))

    mainScene.setCamera(camera_obj)
    airplane.addChild(camera_obj)

    terrain = Terrain(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]))
    
    mainScene.addObject(terrain)
    mainScene.addObject(airplane)
    
    mainScene.run()

