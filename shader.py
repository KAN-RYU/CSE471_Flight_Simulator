from OpenGL.GL import *
from OpenGL.GLUT import *

def createShader():
    """
    Creates shader program
    """
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

    vertex_shader_src = """
    #version 130

    void main(){
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    """

    fragment_shader_src = """
    #version 130

    out vec4 color;

    uniform vec4 pickingColor;

    void main(){
        color = pickingColor;
    }
    """

    glShaderSource(vertex_shader, vertex_shader_src)
    glShaderSource(fragment_shader, fragment_shader_src)

    glCompileShader(vertex_shader)
    glCompileShader(fragment_shader)

    shaderProgramID = glCreateProgram()

    glAttachShader(shaderProgramID, vertex_shader)
    glAttachShader(shaderProgramID, fragment_shader)

    glLinkProgram(shaderProgramID)

    PickingColor = glGetUniformLocation(shaderProgramID, "pickingColor")

    return shaderProgramID, PickingColor
