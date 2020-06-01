"""
MIT License

Copyrights © 2020, Philippe-Henri Gosselin.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the “Software”), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

The Software is provided “as is”, without warranty of any kind, express or 
implied, including but not limited to the warranties of merchantability, fitness 
for a particular purpose and noninfringement. In no event shall the authors or 
copyright holders be liable for any claim, damages or other liability, whether 
in an action of contract, tort or otherwise, arising from, out of or in 
connection with the software or the use or other dealings in the Software.

Except as contained in this notice, the name of Philippe-Henri Gosselin shall 
not be used in advertising or otherwise to promote the sale, use or other 
dealings in this Software without prior written authorization from 
Philippe-Henri Gosselin.

"""
from .Command import Command

from pygame.math import Vector2

class MoveBulletCommand(Command):
    def __init__(self,state,bullet):
        self.state = state
        self.bullet = bullet
    def run(self):
        direction = (self.bullet.endPosition - self.bullet.startPosition).normalize()
        newPos = self.bullet.position + self.state.bulletSpeed * direction
        newCenterPos = newPos + Vector2(0.5,0.5)
        # If the bullet goes outside the world, destroy it
        if not self.state.isInside(newPos):
            self.bullet.status = "destroyed"
            return
        # If the bullet goes towards the target cell, destroy it
        if ((direction.x >= 0 and newPos.x >= self.bullet.endPosition.x) \
        or (direction.x < 0 and newPos.x <= self.bullet.endPosition.x)) \
        and ((direction.y >= 0 and newPos.y >= self.bullet.endPosition.y) \
        or (direction.y < 0 and newPos.y <= self.bullet.endPosition.y)):
            self.bullet.status = "destroyed"
            return
        # If the bullet is outside the allowed range, destroy it
        if newPos.distance_to(self.bullet.startPosition) >= self.state.bulletRange:  
            self.bullet.status = "destroyed"
            return
        # If the bullet hits a unit, destroy the bullet and the unit 
        unit = self.state.findLiveUnit(newCenterPos)
        if not unit is None and unit != self.bullet.unit:
            self.bullet.status = "destroyed"
            unit.status = "destroyed"
            self.state.notifyUnitDestroyed(unit)
            return
        # Nothing happends, continue bullet trajectory
        self.bullet.position = newPos
