from .Layer import Layer

import pygame
from pygame.math import Vector2

class ArrayLayer(Layer):
    def __init__(self,cellSize,imageFile,gameState,array,surfaceFlags=pygame.SRCALPHA):
        super().__init__(cellSize,imageFile)
        self.gameState = gameState
        self.array = array
        self.surface = None
        self.surfaceFlags = surfaceFlags
        
    def setTileset(self,cellSize,imageFile):
        super().setTileset(cellSize,imageFile)
        self.surface = None
        
    def render(self,surface):
        if self.surface is None:
            self.surface = pygame.Surface(surface.get_size(),flags=self.surfaceFlags)
            for y in range(self.gameState.worldHeight):
                for x in range(self.gameState.worldWidth):
                    tile = self.array[y][x]
                    if not tile is None:
                        self.renderTile(self.surface,Vector2(x,y),tile)
        surface.blit(self.surface,(0,0))