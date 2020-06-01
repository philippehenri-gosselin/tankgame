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
from .GameMode import GameMode

from state import GameState
from layer import ArrayLayer, UnitsLayer, BulletsLayer, ExplosionsLayer, SoundLayer
from command import MoveCommand, TargetCommand, ShootCommand, MoveBulletCommand, DeleteDestroyedCommand

import pygame
from pygame.math import Vector2

class PlayGameMode(GameMode):
    def __init__(self):
        super().__init__()
        # Game state
        self.gameState = GameState()
        
        # Rendering properties
        self.cellSize = Vector2(64,64)        

        # Layers
        self.layers = [
            ArrayLayer(self.cellSize,"assets/level/ground.png",self.gameState,self.gameState.ground,0),
            ArrayLayer(self.cellSize,"assets/level/walls.png",self.gameState,self.gameState.walls),
            UnitsLayer(self.cellSize,"assets/level/units.png",self.gameState,self.gameState.units),
            BulletsLayer(self.cellSize,"assets/level/explosions.png",self.gameState,self.gameState.bullets),
            ExplosionsLayer(self.cellSize,"assets/level/explosions.png"),
            SoundLayer("assets/sound/170274__knova__rifle-fire-synthetic.wav","assets/sound/110115__ryansnook__small-explosion.wav")
        ]
        
        # All layers listen to game state events
        for layer in self.layers:
            self.gameState.addObserver(layer)

        # Controls
        self.playerUnit = self.gameState.units[0]
        self.gameOver = False
        self.commands = [ ]
        
    @property
    def cellWidth(self):
        return int(self.cellSize.x)

    @property
    def cellHeight(self):
        return int(self.cellSize.y)

    def processInput(self):
        # Pygame events (close, keyboard and mouse click)
        moveVector = Vector2()
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    self.notifyQuitRequested()
                    break
                elif event.key == pygame.K_ESCAPE:
                    self.notifyShowMenuRequested()
                    break
                elif event.key == pygame.K_RIGHT:
                    moveVector.x = 1
                elif event.key == pygame.K_LEFT:
                    moveVector.x = -1
                elif event.key == pygame.K_DOWN:
                    moveVector.y = 1
                elif event.key == pygame.K_UP:
                    moveVector.y = -1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseClicked = True

        # If the game is over, all commands creations are disabled
        if self.gameOver:
            return
                    
        # Keyboard controls the moves of the player's unit
        if moveVector.x != 0 or moveVector.y != 0:
            self.commands.append(
                MoveCommand(self.gameState,self.playerUnit,moveVector)
            )
                    
        # Mouse controls the target of the player's unit
        mousePos = pygame.mouse.get_pos()                    
        targetCell = Vector2()
        targetCell.x = mousePos[0] / self.cellWidth - 0.5
        targetCell.y = mousePos[1] / self.cellHeight - 0.5
        command = TargetCommand(self.gameState,self.playerUnit,targetCell)
        self.commands.append(command)

        # Shoot if left mouse was clicked
        if mouseClicked:
            self.commands.append(
                ShootCommand(self.gameState,self.playerUnit)
            )
                
        # Other units always target the player's unit and shoot if close enough
        for unit in self.gameState.units:
            if unit != self.playerUnit:
                self.commands.append(
                    TargetCommand(self.gameState,unit,self.playerUnit.position)
                )
                if unit.position.distance_to(self.playerUnit.position) <= self.gameState.bulletRange:
                    self.commands.append(
                        ShootCommand(self.gameState,unit)
                    )
                
        # Bullets automatic movement
        for bullet in self.gameState.bullets:
            self.commands.append(
                MoveBulletCommand(self.gameState,bullet)
            )
            
        # Delete any destroyed bullet
        self.commands.append(
            DeleteDestroyedCommand(self.gameState.bullets)
        )
                    
    def update(self):
        for command in self.commands:
            command.run()
        self.commands.clear()
        self.gameState.epoch += 1
        
        # Check game over
        if self.playerUnit.status != "alive":
            self.gameOver = True
            self.notifyGameLost()
        else:
            oneEnemyStillLives = False
            for unit in self.gameState.units:
                if unit == self.playerUnit:
                    continue
                if unit.status == "alive":
                    oneEnemyStillLives = True
                    break
            if not oneEnemyStillLives:
                self.gameOver = True
                self.notifyGameWon()
        
    def render(self, window):
        for layer in self.layers:
            layer.render(window)
