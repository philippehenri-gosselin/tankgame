from .Layer import Layer

import math
from pygame.math import Vector2

class UnitsLayer(Layer):
    def __init__(self,cellSize,imageFile,gameState,units):
        super().__init__(cellSize,imageFile)
        self.gameState = gameState
        self.units = units
        
    def render(self,surface):
        for unit in self.units:
            self.renderTile(surface,unit.position,unit.tile,unit.orientation)
            if unit.status == "alive":
                size = unit.weaponTarget - unit.position
                angle = math.atan2(-size.x,-size.y) * 180 / math.pi
                self.renderTile(surface,unit.position,Vector2(0,6),angle)