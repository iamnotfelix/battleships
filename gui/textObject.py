

class TextObject:

    def __init__(self, font, text, position):
        self.__font = font
        self.__position = position
        self.__surface = self.__font.render(text, True, (0, 0, 0))

    @property
    def font(self):
        return self.__font

    @property
    def surface(self):
        return self.__surface

    @property
    def position(self):
        return self.__position
