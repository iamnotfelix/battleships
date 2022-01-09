import pygame
from domain.orientation import Orientation


class GameObject:

    def __init__(self, file_path, position, size=None):
        self.__surface = pygame.image.load(file_path)
        self.__rect = self.__surface.get_rect()
        self.__rect.x, self.__rect.y = position
        self.__orientation = Orientation.Horizontal
        self.__size = size
        self.__placed = False

    @property
    def surface(self):
        return self.__surface

    @property
    def rect(self):
        return self.__rect

    @property
    def x(self):
        return self.__rect.x

    @property
    def y(self):
        return self.__rect.y

    @property
    def position(self):
        return self.__rect.x, self.__rect.y

    @property
    def orientation(self):
        return self.__orientation

    @property
    def size(self):
        return self.__size

    @property
    def placed(self):
        return self.__placed

    @placed.setter
    def placed(self, value):
        self.__placed = value

    @x.setter
    def x(self, value):
        self.__rect.x = value

    @y.setter
    def y(self, value):
        self.__rect.y = value

    def rotate(self):
        self.__surface = pygame.transform.rotate(self.__surface, 90)
        position = self.__rect.center
        self.__rect = self.__surface.get_rect()
        self.__rect.center = position
        self.__orientation = Orientation.Vertical if self.__orientation == Orientation.Horizontal else Orientation.Horizontal
