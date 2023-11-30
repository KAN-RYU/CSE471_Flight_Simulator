from SGEngine.gameobject import *
from SGEngine.rigidbody import RigidBody
from SGEngine.model import Model
from scripts.airplane import AirplaneController

class Airplane(GameObject):
    def __init__(self, position=np.zeros(3), rotation=np.zeros(3), scale=np.ones(3)):
        super().__init__(position, rotation, scale)
        self.rb = RigidBody(mass=20000, inertia=np.array([[10, 0, 0], [0, 10, 0], [0, 0, 10]]), position=position, rotation=Quaternion.from_euler(*rotation))
        self.addComponent(self.rb)
        self.addComponent(AirplaneController())

    def init(self):
        super().init()
        self.model = Model("models/B17GREEN.obj")
        
    def drawSelf(self):
        glPushMatrix()
        glMultMatrixd(self.worldMat.T)
        self.model.draw()
        glPopMatrix()

        