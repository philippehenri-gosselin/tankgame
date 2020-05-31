from .Layer import Layer

import pygame

class SoundLayer(Layer):
    def __init__(self,fireFile,explosionFile):
        self.fireSound = pygame.mixer.Sound(fireFile)
        self.fireSound.set_volume(0.2)
        self.explosionSound = pygame.mixer.Sound(explosionFile)
        self.explosionSound.set_volume(0.2)
    
    def unitDestroyed(self,unit):
        self.explosionSound.play()

    def bulletFired(self,unit):
        self.fireSound.play()

    def render(self,surface):
        pass