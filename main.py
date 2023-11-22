from SGEngine.scene import Scene
from SGEngine.gameobject import *
from SGEngine.camera import Camera
from SGEngine.rigidbody import RigidBody
from SGEngine.quaternion import *
from scripts.fps import FPSController
from scripts.airplane import AirplaneController
from scripts.terrain import Terrain
import numpy as np

if __name__ == "__main__":
    mainScene = Scene(1280, 720)
    
    # cube = Cube(position=np.array([0, 0.5, 0]), rotation=np.array([0, 0, 0]))
    # rb = RigidBody(inertia=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    # rb.hasGravity = False
    # rb.mass = 1000
    # cube.addComponent(rb)
    # cube.addComponent(AirplaneController())
    
    # cube.addComponent(FPSController())
    # plane = Plane(scale=np.array([10000, 1, 10000]))
    camera_obj = GameObject(position=np.array([-128, 64, -128]), rotation=np.array([np.pi/8, np.pi/4, 0]))
    camera_obj.addComponent(Camera(far = 2048))
    camera_obj.addComponent(FPSController())
    # cube.addChild(camera_obj)
    mainScene.setCamera(camera_obj)
    mainScene.addObject(camera_obj)
    
    terrain = Terrain(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]))
    
    mainScene.addObject(terrain)
    
    # mainScene.addObject(cube)
    # mainScene.addObject(plane)
    
    mainScene.run()