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
        