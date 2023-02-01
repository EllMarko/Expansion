class Case():

    def __init__(self, pawnNumber: int, coordinates: tuple, player: object) -> None:
        self.__pawnNumber = pawnNumber
        self.__coordinates = coordinates
        self.__player = player

    def getPawnNumber(self) -> int:
        return self.__pawnNumber

    def getCoordinates(self) -> int:
        return self.__coordinates

    def getPlayer(self) -> int:
        return self.__player

    def setPawnNumber(self, value: int) -> None:
        self.__pawnNumber = value

    def setCoordinates(self, value: int) -> None:
        self.__coordinates = value

    def setPlayer(self, value: object) -> None:
        self.__player = value

    def __repr__(self) -> str:
        return str((self.getPawnNumber(), (self.getPlayer().getNumber())))
