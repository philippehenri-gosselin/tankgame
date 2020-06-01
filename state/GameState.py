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
