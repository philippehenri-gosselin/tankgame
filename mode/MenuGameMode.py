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

import pygame

class MenuGameMode(GameMode):
    def __init__(self):        
        super().__init__()
        # Font
        self.titleFont = pygame.font.Font("assets/ui/BD_Cartoon_Shout.ttf", 72)
        self.itemFont = pygame.font.Font("assets/ui/BD_Cartoon_Shout.ttf", 48)
        
        # Menu items
        self.menuItems = [
            {
                'title': 'Level 1',
                'action': lambda: self.notifyLoadLevelRequested("assets/level/level1.tmx")
            },
            {
                'title': 'Level 2',
                'action': lambda: self.notifyLoadLevelRequested("assets/level/level2.tmx")
            },
            {
                'title': 'Level 3',
                'action': lambda: self.notifyLoadLevelRequested("assets/level/level3.tmx")
            },
            {
                'title': 'Quit',
                'action': lambda: self.notifyQuitRequested()
            }
        ]        

        # Compute menu width
        self.menuWidth = 0
        for item in self.menuItems:
            surface = self.itemFont.render(item['title'], True, (200, 0, 0))
            self.menuWidth = max(self.menuWidth, surface.get_width())
            item['surface'] = surface        
        
        self.currentMenuItem = 0
        self.menuCursor = pygame.image.load("assets/ui/cursor.png")        

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.notifyQuitRequested()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.notifyShowGameRequested()
                elif event.key == pygame.K_DOWN:
                    if self.currentMenuItem < len(self.menuItems) - 1:
                        self.currentMenuItem += 1
                elif event.key == pygame.K_UP:
                    if self.currentMenuItem > 0:
                        self.currentMenuItem -= 1
                elif event.key == pygame.K_RETURN:
                    menuItem = self.menuItems[self.currentMenuItem]
                    try:
                        menuItem['action']()
                    except Exception as ex:
                        print(ex)
                    
    def update(self):
        pass
        
    def render(self, window):
        # Initial y
        y = 50
        
        # Title
        surface = self.titleFont.render("TANK BATTLEGROUNDS !!", True, (200, 0, 0))
        x = (window.get_width() - surface.get_width()) // 2
        window.blit(surface, (x, y))
        y += (200 * surface.get_height()) // 100
        
        # Draw menu items
        x = (window.get_width() - self.menuWidth) // 2
        for index, item in enumerate(self.menuItems):
            # Item text
            surface = item['surface']
            window.blit(surface, (x, y))
            
            # Cursor
            if index == self.currentMenuItem:
                cursorX = x - self.menuCursor.get_width() - 10
                cursorY = y + (surface.get_height() - self.menuCursor.get_height()) // 2
                window.blit(self.menuCursor, (cursorX, cursorY))
            
            y += (120 * surface.get_height()) // 100      
