import numpy as np
from typing import Tuple
from lib.gameobject import *
from lib.gameobject import ComponentType, GameObject
from lib.quaternion import *

class RigidBody(Component):
    def __init__(self, 
                 mass: float = 1.0, 
                 inertia: np.ndarray((3, 3)) = np.zeros((3, 3)), 
                 position: np.ndarray = np.zeros(3), 
                 velocity: np.ndarray = np.zeros(3),
                 rotation: Quaternion = Quaternion.identity(), 
                 angular_velocity: np.ndarray = np.zeros(3)):
        self.mass = mass
        self.inertia = inertia
        self.inverse_inertia = np.linalg.inv(inertia)
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        self.angular_velocity = angular_velocity
        self.hasGravity = True
        self.gravity = np.array([0, -9.8, 0])

        self.force = np.zeros(3)
        self.torque = np.zeros(3)

    def getType(self) -> ComponentType:
        return ComponentType.RIGIDBODY
    
    def register(self, gameObject: GameObject):
        super().register(gameObject)
        gameObject.updateCallbacks.append(self.update)

    def update(self, obj: GameObject, dt: float):
        if self.hasGravity:
            self.force += self.mass * self.gravity
        
        acceleration = self.force / self.mass

        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        delta_angular_velocity = self.inverse_inertia @ self.torque * dt
        self.angular_velocity += delta_angular_velocity

        quaternion_rate = Quaternion(0, *self.angular_velocity) * self.rotation
        self.rotation = self.rotation + quaternion_rate * 0.5 * dt
        self.rotation.normalize()

        self.force = np.zeros(3)
        self.torque = np.zeros(3)

        obj.setPosition(self.position)
        obj.setRotation(self.rotation)

    def applyForce(self, force, point):
        self.force += force
        self.torque += np.cross(point - self.position, force)

    def applyRelativeForce(self, force):
        self.force += self.object.getLocalVec(force)

    def applyImpulse(self, impulse, point):
        self.velocity += impulse / self.mass
        self.angular_velocity += np.cross(point - self.position, impulse) / self.inertia

    def applyRelativeTorque(self, torque):
        self.torque += torque
    
    def applyRelativeTorqueStep(self, torque):
        delta_angular_velocity = self.inverse_inertia @ torque
        self.angular_velocity += delta_angular_velocity

        quaternion_rate = Quaternion(0, *self.angular_velocity) * self.rotation
        self.rotation = self.rotation + quaternion_rate * 0.5
        self.rotation.normalize()

    def applyAngularImpulse(self, angular_impulse):
        self.angular_velocity += angular_impulse / self.inertia