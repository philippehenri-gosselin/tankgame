from .Layer import Layer

import math
from pygame.math import Vector2

class ExplosionsLayer(Layer):
    def __init__(self,cellSize,imageFile):
        super().__init__(cellSize,imageFile)
        self.explosions = []
        self.maxFrameIndex = 27
        
    def add(self,position):
        self.explosions.append({
            'position': position,
            'frameIndex': 0
        })

    def unitDestroyed(self,unit):
        self.add(unit.position)
        
    def render(self,surface):
        for explosion in self.explosions:
            frameIndex = math.floor(explosion['frameIndex'])
            self.renderTile(surface,explosion['position'],Vector2(frameIndex,4))
            explosion['frameIndex'] += 0.5
        self.explosions = [ explosion for explosion in self.explosions if explosion['frameIndex'] < self.maxFrameIndex ]