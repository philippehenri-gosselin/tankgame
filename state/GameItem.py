
class GameItem():
    def __init__(self,state,position,tile):
        self.state = state
        self.status = "alive"
        self.position = position
        self.tile = tile
        self.orientation = 0   