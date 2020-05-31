class GameMode():
    def __init__(self):
        self.__observers = []
    def addObserver(self, observer):
        self.__observers.append(observer)
    def notifyLoadLevelRequested(self, fileName):
        for observer in self.__observers:
            observer.loadLevelRequested(fileName)
    def notifyWorldSizeChanged(self, worldSize):
        for observer in self.__observers:
            observer.worldSizeChanged(worldSize)
    def notifyShowMenuRequested(self):
        for observer in self.__observers:
            observer.showMenuRequested()
    def notifyShowGameRequested(self):
        for observer in self.__observers:
            observer.showGameRequested()
    def notifyGameWon(self):
        for observer in self.__observers:
            observer.gameWon()
    def notifyGameLost(self):
        for observer in self.__observers:
            observer.gameLost()
    def notifyQuitRequested(self):
        for observer in self.__observers:
            observer.quitRequested()
        
    def processInput(self):
        raise NotImplementedError()
    def update(self):
        raise NotImplementedError()
    def render(self, window):
        raise NotImplementedError()