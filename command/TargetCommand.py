from .Command import Command

class TargetCommand(Command):
    def __init__(self,state,unit,target):
        self.state = state
        self.unit = unit
        self.target = target
    def run(self):
        self.unit.weaponTarget = self.target