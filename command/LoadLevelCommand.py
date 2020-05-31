from .Command import Command

from state import Unit

import os
import tmx
from pygame.math import Vector2

class LoadLevelCommand(Command)       :
    def __init__(self,gameMode,fileName):
        self.gameMode = gameMode
        self.fileName = fileName
        
    def decodeLayer(self,tileMap,layer):
        """
        Decode layer and check layer properties
        
        Returns the corresponding tileset
        """
        if not isinstance(layer,tmx.Layer):
            raise RuntimeError("Error in {}: invalid layer type".format(self.fileName))
        if len(layer.tiles) != tileMap.width * tileMap.height:
            raise RuntimeError("Error in {}: invalid tiles count".format(self.fileName))
        
        # Guess which tileset is used by this layer
        gid = None
        for tile in layer.tiles:
            if tile.gid != 0:
                gid = tile.gid
                break
        if gid is None:
            if len(tileMap.tilesets) == 0:
                raise RuntimeError("Error in {}: no tilesets".format(self.fileName))
            tileset = tileMap.tilesets[0]
        else:
            tileset = None
            for t in tileMap.tilesets:
                if gid >= t.firstgid and gid < t.firstgid+t.tilecount:
                    tileset = t
                    break
            if tileset is None:
                raise RuntimeError("Error in {}: no corresponding tileset".format(self.fileName))
            
        # Check the tileset
        if tileset.columns <= 0:
            raise RuntimeError("Error in {}: invalid columns count".format(self.fileName))
        if tileset.image.data is not None:
            raise RuntimeError("Error in {}: embedded tileset image is not supported".format(self.fileName))
            
        return tileset
        
    def decodeArrayLayer(self,tileMap,layer):
        """
        Create an array from a tileMap layer
        """        
        tileset = self.decodeLayer(tileMap,layer)
        
        array = [ None ] * tileMap.height
        for y in range(tileMap.height):
            array[y] = [ None ] * tileMap.width
            for x in range(tileMap.width):
                tile = layer.tiles[x + y*tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                array[y][x] = Vector2(tileX,tileY)

        return tileset, array
    
    def decodeUnitsLayer(self,state,tileMap,layer):
        """
        Create a list from a tileMap layer
        """        
        tileset = self.decodeLayer(tileMap,layer)

        units = []
        for y in range(tileMap.height):
            for x in range(tileMap.width):
                tile = layer.tiles[x + y*tileMap.width]
                if tile.gid == 0:
                    continue
                lid = tile.gid - tileset.firstgid
                if lid < 0 or lid >= tileset.tilecount:
                    raise RuntimeError("Error in {}: invalid tile id".format(self.fileName))
                tileX = lid % tileset.columns
                tileY = lid // tileset.columns
                unit = Unit(state,Vector2(x,y),Vector2(tileX,tileY))
                units.append(unit)

        return tileset, units
        
        
    def run(self):
        # Load map
        if not os.path.exists(self.fileName):
            raise RuntimeError("No file {}".format(self.fileName))
        tileMap = tmx.TileMap.load(self.fileName)
        
        # Check main properties
        if tileMap.orientation != "orthogonal":
            raise RuntimeError("Error in {}: invalid orientation".format(self.fileName))
            
        if len(tileMap.layers) != 5:
            raise RuntimeError("Error in {}: 5 layers are expected".format(self.fileName))

        # World size
        state = self.gameMode.gameState
        state.worldSize = Vector2(tileMap.width,tileMap.height)    

        # Ground layer
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[0])
        cellSize = Vector2(tileset.tilewidth,tileset.tileheight)
        state.ground[:] = array
        imageFile = tileset.image.source
        self.gameMode.layers[0].setTileset(cellSize,imageFile)

        # Walls layer
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[1])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.walls[:] = array
        imageFile = tileset.image.source
        self.gameMode.layers[1].setTileset(cellSize,imageFile)

        # Units layer
        tanksTileset, tanks = self.decodeUnitsLayer(state,tileMap,tileMap.layers[2])
        towersTileset, towers = self.decodeUnitsLayer(state,tileMap,tileMap.layers[3])
        if tanksTileset != towersTileset:
            raise RuntimeError("Error in {}: tanks and towers tilesets must be the same".format(self.fileName))
        if tanksTileset.tilewidth != cellSize.x or tanksTileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.units[:] = tanks + towers
        cellSize = Vector2(tanksTileset.tilewidth,tanksTileset.tileheight)
        imageFile = tanksTileset.image.source
        self.gameMode.layers[2].setTileset(cellSize,imageFile)

        # Player units
        self.gameMode.playerUnit = tanks[0]      
        
        # Explosions layers
        tileset, array = self.decodeArrayLayer(tileMap,tileMap.layers[4])
        if tileset.tilewidth != cellSize.x or tileset.tileheight != cellSize.y:
            raise RuntimeError("Error in {}: tile sizes must be the same in all layers".format(self.fileName))
        state.bullets.clear()
        imageFile = tileset.image.source
        self.gameMode.layers[3].setTileset(cellSize,imageFile)
        
        # Window
        worldSize = state.worldSize.elementwise() * cellSize
        self.gameMode.notifyWorldSizeChanged(worldSize)
        
        # Resume game
        self.gameMode.gameOver = False