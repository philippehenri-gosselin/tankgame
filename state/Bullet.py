from .GameItem import GameItem

from pygame.math import Vector2

class Bullet(GameItem):
    def __init__(self,state,unit):
        super().__init__(state,unit.position,Vector2(2,1))
        self.unit = unit
        self.startPosition = unit.position
        self.endPosition = unit.weaponTarget