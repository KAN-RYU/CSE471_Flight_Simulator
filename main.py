from SGEngine.scene import Scene
from SGEngine.gameobject import *
from SGEngine.camera import Camera
from SGEngine.rigidbody import RigidBody
from SGEngine.quaternion import *
from scripts.fps import FPSController
from scripts.airplane import AirplaneController
from scripts.terrain import Terrain
from scripts.camera import CameraController
import numpy as np

if __name__ == "__main__":
    mainScene = Scene(1280, 720)
    
    cube = Cube()
    rb = RigidBody(position=np.array([0, 100, 0], dtype=np.float32), inertia=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    # rb.hasGravity = False
    rb.mass = 100
    cube.addComponent(rb)
    cube.addComponent(AirplaneController())
    
    # cube.addComponent(FPSController())
    # plane = Plane(scale=np.array([10000, 1, 10000]))
    # camera_obj = GameObject(position=np.array([-128, 64, -128]), rotation=np.array([np.pi/8, np.pi/4, 0]))
    camera_obj = GameObject(position=np.array([0, 2, -6]), rotation=np.array([np.pi/8, 0, 0]))
    camera_obj.addComponent(Camera(far = 256))
    # camera_obj.addComponent(CameraController(cube))
    # camera_obj.addComponent(FPSController())
    mainScene.setCamera(camera_obj)
    cube.addChild(camera_obj)    
    terrain = Terrain(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]))
    
    mainScene.addObject(terrain)
    
    mainScene.addObject(cube)
    
    # mainScene.addObject(plane)
    
    mainScene.run()