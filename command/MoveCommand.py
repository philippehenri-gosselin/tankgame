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

class MoveCommand(Command):
    """
    This command moves a unit in a given direction
    """
    def __init__(self,state,unit,moveVector):
        self.state = state
        self.unit = unit
        self.moveVector = moveVector
    def run(self):
        unit = self.unit
        
        # Destroyed units can't move
        if unit.status != "alive":
            return

        # Update unit orientation
        if self.moveVector.x < 0: 
            unit.orientation = 90
        elif self.moveVector.x > 0: 
            unit.orientation = -90
        if self.moveVector.y < 0: 
            unit.orientation = 0
        elif self.moveVector.y > 0: 
            unit.orientation = 180
        
        # Compute new tank position
        newPos = unit.position + self.moveVector

        # Don't allow positions outside the world
        if not self.state.isInside(newPos):
            return

        # Don't allow wall positions
        if not self.state.walls[int(newPos.y)][int(newPos.x)] is None:
            return

        # Don't allow other unit positions 
        unitIndex = self.state.findUnit(newPos)
        if not unitIndex is None:
                return

        unit.position = newPos
        
