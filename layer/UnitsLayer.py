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
