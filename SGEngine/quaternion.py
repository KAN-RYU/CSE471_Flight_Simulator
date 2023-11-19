import math
import numpy as np

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def identity(cls):
        # 항등원(Identity) Quaternion을 반환
        return cls(1.0, 0.0, 0.0, 0.0)

    @classmethod
    def from_axis_angle(cls, axis, angle):
        # 축과 각도를 사용하여 Quaternion을 생성
        angle /= 2
        sin_angle = math.sin(angle)
        return cls(math.cos(angle), axis[0] * sin_angle, axis[1] * sin_angle, axis[2] * sin_angle)

    @classmethod
    def from_euler(cls, roll, pitch, yaw):
        # Roll, pitch, yaw Euler 각도를 사용하여 Quaternion을 생성
        roll /= 2
        pitch /= 2
        yaw /= 2

        cy = math.cos(yaw)
        sy = math.sin(yaw)
        cp = math.cos(pitch)
        sp = math.sin(pitch)
        cr = math.cos(roll)
        sr = math.sin(roll)

        qw = cr * cp * cy + sr * sp * sy
        qx = sr * cp * cy - cr * sp * sy
        qy = cr * sp * cy + sr * cp * sy
        qz = cr * cp * sy - sr * sp * cy

        return cls(qw, qx, qy, qz)
    
    @classmethod
    def from_euler_vec(cls, rotation):
        return cls.from_euler(rotation[0], rotation[1], rotation[2])
    
    def to_euler(self):
        # Quaternion을 Roll, Pitch, Yaw Euler 각도로 변환
        t0 = 2.0 * (self.w * self.x + self.y * self.z)
        t1 = 1.0 - 2.0 * (self.x**2 + self.y**2)
        roll_x = math.atan2(t0, t1)

        t2 = 2.0 * (self.w * self.y - self.z * self.x)
        t2 = 1.0 if t2 > 1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = 2.0 * (self.w * self.z + self.x * self.y)
        t4 = 1.0 - 2.0 * (self.y**2 + self.z**2)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z
    
    def to_rotation_matrix(self):
        # Quaternion을 3x3 회전 행렬로 변환
        qw, qx, qy, qz = self.w, self.x, self.y, self.z

        # Normalization to handle precision errors
        norm = math.sqrt(qw**2 + qx**2 + qy**2 + qz**2)
        qw /= norm
        qx /= norm
        qy /= norm
        qz /= norm

        # Calculate rotation matrix elements
        r11 = 1.0 - 2.0 * (qy**2 + qz**2)
        r12 = 2.0 * (qx*qy - qz*qw)
        r13 = 2.0 * (qx*qz + qy*qw)

        r21 = 2.0 * (qx*qy + qz*qw)
        r22 = 1.0 - 2.0 * (qx**2 + qz**2)
        r23 = 2.0 * (qy*qz - qx*qw)

        r31 = 2.0 * (qx*qz - qy*qw)
        r32 = 2.0 * (qy*qz + qx*qw)
        r33 = 1.0 - 2.0 * (qx**2 + qy**2)

        return np.array([[r11, r12, r13, 0],
                         [r21, r22, r23, 0],
                         [r31, r32, r33, 0],
                         [0, 0, 0, 1]])

    def normalize(self):
        # Quaternion을 정규화
        magnitude = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        self.w /= magnitude
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude

    def conjugate(self):
        # 켤레 Quaternion 계산
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def multiply(self, other):
        # Quaternion 곱셈
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)
    
    def __add__(self, other):
        # Quaternion 덧셈
        return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        # Quaternion 곱셈
        if isinstance(other, Quaternion):
            return self.multiply(other)
        elif isinstance(other, (int, float)):
            return Quaternion(self.w * other, self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Quaternion can only be multiplied by a Quaternion or a scalar")
        
    def rotate_vector(self, vector):
        # Quaternion으로 벡터 회전
        q_vector = Quaternion(0, vector[0], vector[1], vector[2])
        rotated_vector = (self * q_vector * self.conjugate()).xyz
        return rotated_vector
    
    @property
    def xyz(self):
        # Quaternion의 x, y, z 값만 반환
        return self.x, self.y, self.z