from lib.scene import Scene
from lib.gameobject import *
from lib.camera import Camera
from lib.rigidbody import RigidBody
from lib.quaternion import *
from scripts.fps import FPSController
from scripts.airplane import AirplaneController
import numpy as np

if __name__ == "__main__":
    mainScene = Scene(800, 600)
    cube = Cube(position=np.array([0, 0.5, 0]), rotation=np.array([0, 0, 0]))
    rb = RigidBody(inertia=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
    rb.hasGravity = False
    rb.mass = 1000
    cube.addComponent(rb)
    cube.addComponent(AirplaneController())
    # cube.addComponent(FPSController())
    plane = Plane(scale=np.array([10000, 1, 10000]))
    camera_obj = GameObject(position=np.array([0, 2, -8]), rotation=np.array([np.pi / 20, 0, 0]))
    camera_obj.addComponent(Camera())
    # camera_obj.addComponent(FPSController())
    cube.addChild(camera_obj)
    mainScene.setCamera(camera_obj)
    mainScene.addObject(camera_obj)
    mainScene.addObject(cube)
    mainScene.addObject(plane)
    mainScene.run()