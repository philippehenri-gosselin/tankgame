from mode import GameModeObserver, MenuGameMode, PlayGameMode, MessageGameMode
from command import LoadLevelCommand

import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

class UserInterface(GameModeObserver):
    def __init__(self):
        # Window
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Discover Python & Patterns - https://www.patternsgameprog.com")
        pygame.display.set_icon(pygame.image.load("assets/ui/icon.png"))
        
        # Modes
        self.playGameMode = None
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'
        
        # Music
        pygame.mixer.music.load("assets/music/17718_1462204250.mp3")
        pygame.mixer.music.play(loops=-1)
        
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True        
        
    def gameWon(self):
        self.showMessage("Victory !")
        pygame.mixer.music.load("assets/music/17382_1461858477.mp3")
        pygame.mixer.music.play(loops=-1)
    
    def gameLost(self):
        self.showMessage("GAME OVER")
        pygame.mixer.music.load("assets/music/17675_1462199580.mp3")
        pygame.mixer.music.play(loops=-1)
        
    def loadLevelRequested(self, fileName):
        if self.playGameMode is None:
            self.playGameMode = PlayGameMode()
            self.playGameMode.addObserver(self)
        self.playGameMode.commands.append(LoadLevelCommand(self.playGameMode,fileName))
        try:
            self.playGameMode.update()
            self.currentActiveMode = 'Play'
        except Exception as ex:
            print(ex)
            self.playGameMode = None
            self.showMessage("Level loading failed :-(")

        pygame.mixer.music.load("assets/music/17687_1462199612.mp3")
        pygame.mixer.music.play(loops=-1)

    def worldSizeChanged(self, worldSize):
        self.window = pygame.display.set_mode((int(worldSize.x),int(worldSize.y)))
        
    def showGameRequested(self):
        if self.playGameMode is not None:
            self.currentActiveMode = 'Play'

    def showMenuRequested(self):
        self.overlayGameMode = MenuGameMode()
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'
        
    def showMessage(self, message):
        self.overlayGameMode = MessageGameMode(message)
        self.overlayGameMode.addObserver(self)
        self.currentActiveMode = 'Overlay'
        
    def quitRequested(self):
        self.running = False
       
    def run(self):
        while self.running:
            # Inputs and updates are exclusives
            if self.currentActiveMode == 'Overlay':
                self.overlayGameMode.processInput()
                self.overlayGameMode.update()
            elif self.playGameMode is not None:
                self.playGameMode.processInput()
                try:
                    self.playGameMode.update()
                except Exception as ex:
                    print(ex)
                    self.playGameMode = None
                    self.showMessage("Error during the game update...")
                    
            # Render game (if any), and then the overlay (if active)
            if self.playGameMode is not None:
                self.playGameMode.render(self.window)
            else:
                self.window.fill((0,0,0))
            if self.currentActiveMode == 'Overlay':
                darkSurface = pygame.Surface(self.window.get_size(),flags=pygame.SRCALPHA)
                pygame.draw.rect(darkSurface, (0,0,0,150), darkSurface.get_rect())
                self.window.blit(darkSurface, (0,0))
                self.overlayGameMode.render(self.window)
                
            # Update display
            pygame.display.update()    
            self.clock.tick(60)
            
     
userInterface = UserInterface()
userInterface.run()
           
pygame.quit()