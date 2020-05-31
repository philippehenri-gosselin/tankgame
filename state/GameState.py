from .Unit import Unit

from pygame.math import Vector2

class GameState():
    def __init__(self):
        self.epoch = 0
        self.worldSize = Vector2(16,10)
        self.ground = [ [ Vector2(5,1) ] * 16 ] * 10
        self.walls = [ [ None ] * 16 ] * 10
        self.units = [ Unit(self,Vector2(8,9),Vector2(1,0)) ]
        self.bullets = [ ]
        self.bulletSpeed = 0.1
        self.bulletRange = 4
        self.bulletDelay = 5
        self.observers = [ ]
    
    @property
    def worldWidth(self):
        """
        Returns the world width as an integer
        """
        return int(self.worldSize.x)
    
    @property
    def worldHeight(self):
        """
        Returns the world height as an integer
        """
        return int(self.worldSize.y)        

    def isInside(self,position):
        """
        Returns true is position is inside the world
        """
        return position.x >= 0 and position.x < self.worldWidth \
           and position.y >= 0 and position.y < self.worldHeight

    def findUnit(self,position):
        """
        Returns the index of the first unit at position, otherwise None.
        """
        for unit in self.units:
            if  int(unit.position.x) == int(position.x) \
            and int(unit.position.y) == int(position.y):
                return unit
        return None
    
    def findLiveUnit(self,position):
        """
        Returns the index of the first live unit at position, otherwise None.
        """
        unit = self.findUnit(position)
        if unit is None or unit.status != "alive":
            return None
        return unit
    
    def addObserver(self,observer):
        """
        Add a game state observer. 
        All observer is notified when something happens (see GameStateObserver class)
        """
        self.observers.append(observer)
        
    def notifyUnitDestroyed(self,unit):
        for observer in self.observers:
            observer.unitDestroyed(unit)

    def notifyBulletFired(self,unit):
        for observer in self.observers:
            observer.bulletFired(unit)