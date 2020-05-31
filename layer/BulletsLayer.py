from .Layer import Layer

class BulletsLayer(Layer):
    def __init__(self,cellSize,imageFile,gameState,bullets):
        super().__init__(cellSize,imageFile)
        self.gameState = gameState
        self.bullets = bullets
        
    def render(self,surface):
        for bullet in self.bullets:
            if bullet.status == "alive":
                self.renderTile(surface,bullet.position,bullet.tile,bullet.orientation)