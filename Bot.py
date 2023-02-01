from Player import Player
import random


class Bot(Player):
    def __init__(self, number: int):
        super().__init__(number)
        self.__level = 0

    def getLevel(self) -> int:
        return self.__level

    def setLevel(self, value: int) -> None:
        self.__level = value

    def randomCoords(self, game: object) -> tuple:
        return (random.randint(0, game.getWidth()-1), random.randint(0, game.getHeight()-1))

    def pickCoordo(self, game: object) -> tuple:
        if self.getLevel() == 0:
            return self.randomCoords(game)
