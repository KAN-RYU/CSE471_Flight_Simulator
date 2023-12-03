from SGEngine.gameobject import *
from SGEngine.rigidbody import RigidBody
from SGEngine.script import Script
from SGEngine.quaternion import *
import numpy as np

def calculateDragCoef(x):
    return np.max([0, np.min([1, 100 / (1 + np.exp(-0.0004 * x)) - 50])])

def calculateDragCoef2(x):
    return np.max([0, np.min([2, 200 / (1 + np.exp(-0.0004 * x)) - 100])])

def calculateLiftCoef(x):
    if x > 90 or x < -90:
        return 0
    return -(1/216000) * x * (x - 90) * (x + 90)

def calculateSteeringCoef(x):
    return 0.1 / (1 + np.exp(-1 * x))

def getScale6(value: np.ndarray(3), posX, negX, posY, negY, posZ, negZ) -> np.ndarray(3):
    result = np.array(value)

    if result[0] > 0:
        result[0] = posX
    elif result[0] < 0:
        result[0] = negX
    
    if result[1] > 0:
        result[1] = posY
    elif result[1] < 0:
        result[1] = negY

    if result[2] > 0:
        result[2] = posZ
    elif result[2] < 0:
        result[2] = negZ

    return result
    

class AirplaneController(Script):
    def __init__(self):
        super().__init__()
        self.rb = None
        self.hInput = 0
        self.vInput = 0
        self.zInput = 0
        self.rollInput = 0
        self.liftPower = 200
        self.rudderPower = 150
        self.inducedDrag = 75
        self.airBrakeDrag = 5
        self.flapsDrag = 5
        self.flapsLiftPower = 150
        self.flapsAoaBias = 0.5
        self.airBrakeEnabled = False
        self.flapsEnabled = True
        self.turnSpeed = np.array([30, 15, 270])
        self.turnAcceleration = np.array([180, 180, 540])

        self.localVelocity = np.zeros(3)
        self.localAngularVelocity = np.zeros(3)

        self.aoa = 0
        self.aoa_yaw = 0

    def Start(self, gameObject: GameObject):
        rb = gameObject.getComponent(ComponentType.RIGIDBODY)
        if not isinstance(rb, RigidBody):
            raise Exception("AirplaneController needs RigidBody component")
        else:
            self.rb = rb

    def Update(self, gameObject: GameObject, dt: float):
        # print(self.object.position)
        self.CalculateState(dt)
        self.CalculateAoA()

        self.updateThrust()
        self.updateLift()
        self.updateSteering(dt)

        self.updateDrag()

    def Keyboard(self, gameObject: GameObject, key: int, x: int, y: int):
        if key == b'w':
            self.vInput = 1
        if key == b's':
            self.vInput = -1
        if key == b'a':
            self.rollInput = -1
        if key == b'd':
            self.rollInput = 1
        if key == b'f':
            self.zInput = 1 - self.zInput
        if key == b'q':
            self.hInput = -1
        if key == b'e':
            self.hInput = 1

        if key == b' ':
            self.airBrakeEnabled = True

        if key == b'c':
            self.flapsEnabled = not self.flapsEnabled

    def KeyboardUp(self, gameObject: GameObject, key: int, x: int, y: int):
        if key == b'w' or key == b's':
            self.vInput = 0
        if key == b'a' or key == b'd':
            self.rollInput = 0
        if key == b'q' or key == b'e':
            self.hInput = 0

        if key == b' ':
            self.airBrakeEnabled = False

    def CalculateState(self, dt):
        rotationMat = self.rb.rotation.to_rotation_matrix()
        invRotationMat = np.linalg.inv(rotationMat)
        self.localVelocity = (invRotationMat @ np.append(self.rb.velocity, [0]))[:3]
        self.localAngularVelocity = (invRotationMat @ np.append(self.rb.angular_velocity, [0]))[:3]

    def CalculateAoA(self):
        if (np.linalg.norm(self.localVelocity) < 0.1):
            self.aoa = 0
            self.aoa_yaw = 0
            return
        self.aoa = np.arctan2(self.localVelocity[1], -self.localVelocity[2])
        self.aoa_yaw = np.arctan2(-self.localVelocity[0], -self.localVelocity[2])

    def calculateLift(self, aoa, rightAxis, liftPower):
        liftVelocity = self.localVelocity - np.dot(self.localVelocity, rightAxis) * rightAxis
        v2 = np.linalg.norm(liftVelocity) ** 2

        liftCoef = calculateLiftCoef(np.rad2deg(aoa))
        liftForce = liftCoef * v2 * liftPower

        # print(f"liftCoef: {liftCoef}, liftForce: {liftForce}, aoa: {np.rad2deg(aoa)}")

        normalizedLiftVelocity = liftVelocity
        if np.linalg.norm(normalizedLiftVelocity) > 0:
            normalizedLiftVelocity = normalizedLiftVelocity / np.linalg.norm(normalizedLiftVelocity)
        liftDir = np.cross(normalizedLiftVelocity, rightAxis)
        lift = liftDir * liftForce

        dragForce = liftCoef * liftCoef * self.inducedDrag
        dragDir = -normalizedLiftVelocity
        inducedDrag = dragDir * v2 * dragForce

        return lift + inducedDrag
    
    def calculateSteering(self, dt, angularVelocity, targetVelocity, acceleration):
        error = targetVelocity - angularVelocity
        accel = acceleration * dt
        return np.min([np.max([error, -accel]), accel])

    def updateThrust(self):
        self.rb.applyRelativeForce(np.array([0, 0, -self.zInput * 200000]))

    def updateDrag(self):
        lv = self.localVelocity
        lvsq = np.linalg.norm(lv) ** 2 
        lv_normalized = np.array(lv)
        if np.linalg.norm(lv_normalized) > 0:
            lv_normalized /= np.linalg.norm(lv_normalized)

        airbrakeDrag = self.airBrakeEnabled * self.airBrakeDrag
        flapsDrag = self.flapsEnabled * self.flapsDrag

        coef = getScale6(lv_normalized, 
                         calculateDragCoef2(np.abs(lv[0])), 
                         calculateDragCoef2(np.abs(lv[0])), 
                         calculateDragCoef2(np.abs(lv[1])), 
                         calculateDragCoef2(np.abs(lv[1])), 
                         calculateDragCoef2(np.abs(lv[2])), 
                         calculateDragCoef(np.abs(lv[2])) + airbrakeDrag + flapsDrag)

        drag = np.linalg.norm(coef) * lvsq
        dragDir = lv_normalized
        if np.linalg.norm(dragDir) > 0:
            dragDir = dragDir / np.linalg.norm(dragDir)
        self.rb.applyRelativeForce(-dragDir * drag)

    def updateLift(self):
        if np.linalg.norm(self.localVelocity) < 1:
            return
        
        flapsLiftPower = self.flapsEnabled * self.flapsLiftPower
        flapsAoaBias = self.flapsEnabled * self.flapsAoaBias

        liftForce = self.calculateLift(self.aoa + np.deg2rad(flapsAoaBias), np.array([1, 0, 0]), self.liftPower + flapsLiftPower)

        yawForce = self.calculateLift(self.aoa_yaw, np.array([0, 1, 0]), self.rudderPower)

        self.rb.applyRelativeForce(liftForce)
        self.rb.applyRelativeForce(yawForce)

    def updateSteering(self, dt):
        speed = np.max([0, self.localVelocity[2]])
        steeringPower = calculateSteeringCoef(speed)

        targetAV = np.array([-self.vInput, -self.hInput, -self.rollInput] * self.turnSpeed * steeringPower)
        av = np.rad2deg(self.localAngularVelocity)

        correction = np.array([self.calculateSteering(dt, av[0], targetAV[0], self.turnAcceleration[0] * steeringPower),
                                 self.calculateSteering(dt, av[1], targetAV[1], self.turnAcceleration[1] * steeringPower),
                                 self.calculateSteering(dt, av[2], targetAV[2], self.turnAcceleration[2] * steeringPower)])
        
        self.rb.applyRelativeTorqueStep(np.deg2rad(correction))
