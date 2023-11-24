from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from SGEngine.shader import Shader
from PIL import Image
import numpy as np

skybox_vertices = np.array([
    -1.0, -1.0,  1.0,#        7--------6
	 1.0, -1.0,  1.0,#       /|       /|
	 1.0, -1.0, -1.0,#      4--------5 |
	-1.0, -1.0, -1.0,#      | |      | |
	-1.0,  1.0,  1.0,#      | 3------|-2
	 1.0,  1.0,  1.0,#      |/       |/
	 1.0,  1.0, -1.0,#      0--------1
	-1.0,  1.0, -1.0
])

skybox_indices = np.array([
    # Right
	1, 2, 6,
	6, 5, 1,
	# Left
	0, 4, 7,
	7, 3, 0,
	# Top
	4, 5, 6,
	6, 7, 4,
	# Bottom
	0, 3, 2,
	2, 1, 0,
	# Back
	0, 1, 5,
	5, 4, 0,
	# Front
	3, 7, 6,
	6, 2, 3
])

imagePaths = [
    "images/right.jpg",
    "images/left.jpg",
    "images/bottom.jpg",
    "images/top.jpg",
    "images/front.jpg",
    "images/back.jpg"
]

class Skybox:
    def __init__(self, scene):
        self.scene = scene
        self.shader = Shader("shaders/skybox.vert", "shaders/skybox.frag")

    def loadTextures(self):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        for i in range(6):
            im = Image.open(imagePaths[i]).rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            width, height = im.size
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, im.tobytes())

    def draw(self):
        glDepthFunc(GL_LEQUAL)
        self.shader.use()
        glActiveTexture(GL_TEXTURE0)
        view = np.eye(4)
        projection = np.eye(4)
        if self.scene.camera is not None:
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(self.scene.camera.fov, self.scene.width / self.scene.height, self.scene.camera.near, self.scene.camera.far)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            glPopMatrix()

        view = self.scene.camera_obj.worldMat
        view[:3, :3] = self.scene.camera_obj.worldMat[:3, :3]
        # flip
        view[1, :] *= -1
        glUniform1i(glGetUniformLocation(self.shader.id, "skybox"), 0)
        glUniformMatrix4fv(glGetUniformLocation(self.shader.id, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(self.shader.id, "projection"), 1, GL_FALSE, projection)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        glPushMatrix()
        glEnableClientState(GL_VERTEX_ARRAY)
        # glScalef(100, 100, 100)
        glVertexPointer(3, GL_FLOAT, 0, skybox_vertices)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, skybox_indices)
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()

        glDepthFunc(GL_LESS)
        glUseProgram(0)