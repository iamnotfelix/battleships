import pygame


class GameObject:

    def __init__(self, file_path, position=(0, 0)):
        self.__surface = pygame.image.load(file_path)
        self.__rect = self.__surface.get_rect()
        self.__rect.x, self.__rect.y = position

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
