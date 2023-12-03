from SGEngine.scene import Scene
from SGEngine.gameobject import *
from SGEngine.camera import Camera
from SGEngine.quaternion import *
from scripts.terrain import Terrain
from scripts.building import Building
from scripts.broken_building import BrokenBuilding
from scripts.fps import FPSController
from scripts.camera import CameraController
from SGEngine.airplane import Airplane
import numpy as np

if __name__ == "__main__":
    mainScene = Scene(1280, 720)
    airplane = Airplane(position=np.array([0.0, 1000.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]))
    mainScene.setAirplane(airplane)
    
    size = 35
    height = 10

    camera_obj = GameObject(position=np.array([-64*size, 50*size, 64*size]), rotation=np.array([-np.pi/8, 0, 0]))
    camera_obj.addComponent(Camera(far = 10000))
    camera_obj.addComponent(CameraController(airplane))
    # camera_obj.addComponent(FPSController())

    mainScene.setCamera(camera_obj)

    terrain = Terrain(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]), size=size, height=height)
    mainScene.setTerrain(terrain)
    
    # sphere = Sphere(np.array([0,0,-1]), np.zeros(3), np.ones(3)*0.2)
    # airplane.addChild(sphere)
    
    # sphere2 = Sphere(np.array([-2.5,0,-0.5]), np.zeros(3), np.ones(3)*0.1)
    # airplane.addChild(sphere2)
    
    # sphere3 = Sphere(np.array([2.5,0, -0.5]), np.zeros(3), np.ones(3)*0.1)
    # airplane.addChild(sphere3)
    
    # sphere4 = Sphere(np.array([0,0,2]), np.zeros(3), np.ones(3)*0.1)
    # airplane.addChild(sphere4)

    building1 = Building(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]), init_pos = np.array([0,-7,-200]))
    building2 = Building(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]), init_pos = np.array([50,-7,200]))
    building3 = Building(position=np.array([0.0, 0.0, 0.0]), rotation=np.array([0.0, 0.0, 0.0]), init_pos = np.array([200,-7,-50]))

    mainScene.setBuilding(building1)
    mainScene.setBuilding(building2)
    mainScene.setBuilding(building3)

    mainScene.addObject(terrain)
    mainScene.addObject(airplane)
    # Error if it exceeds 3 building.
    mainScene.addObject(building1)
    mainScene.addObject(building2)
    mainScene.addObject(building3)

    mainScene.addObject(camera_obj)
    
    
    mainScene.run()

