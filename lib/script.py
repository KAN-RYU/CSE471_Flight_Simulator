from __future__ import annotations

from typing import Callable
from lib.gameobject import *

class Script(Component):
    def __init__(self):
        super().__init__()
    
    def getType(self) -> ComponentType:
        return ComponentType.SCRIPT
    
    def register(self, gameObject: GameObject):
        super().register(gameObject)
        # register callbacks
        gameObject.updateCallbacks.append(self.Update)
        gameObject.keyboardCallbacks.append(self.Keyboard)
        gameObject.keyboardUpCallbacks.append(self.KeyboardUp)
        gameObject.mouseCallbacks.append(self.Mouse)
        gameObject.motionCallbacks.append(self.Motion)
        gameObject.mouseMoveCallbacks.append(self.MouseMove)

    def Start(self, gameObject: GameObject):
        pass

    def Update(self, gameObject: GameObject, dt: float):
        pass

    def Keyboard(self, gameObject: GameObject, key: int, x: int, y: int):
        pass

    def KeyboardUp(self, gameObject: GameObject, key: int, x: int, y: int):
        pass

    def Mouse(self, gameObject: GameObject, button: int, state: int, x: int, y: int):
        pass

    def Motion(self, gameObject: GameObject, x: int, y: int):
        pass

    def MouseMove(self, gameObject: GameObject, x: int, y: int):
        pass
