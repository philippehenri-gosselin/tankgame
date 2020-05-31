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