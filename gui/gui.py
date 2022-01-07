import pygame

from domain.ship import Ship
from domain.position import Position

from gameObject import GameObject
from textObject import TextObject


class State:

    def __init__(self):
        self.dragging = False
        self.ship_dragged = None


class GUI:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Battleships")
        self.__screen = pygame.display.set_mode((1280, 680), pygame.SCALED)
        self.__ships = list()
        self.__sprites = list()
        self.__texts = list()

    def __update_window(self):
        for sprite in self.__sprites:
            self.__screen.blit(sprite.surface, sprite.position)
        for text in self.__texts:
            self.__screen.blit(text.surface, text.position) #(200, 12)
        pygame.display.update()

    def start(self):

        background = GameObject("data/background.png", (0, 0))
        board = GameObject("data/board.png", (100, 90))     # (120, 90)
        ship_5 = GameObject("data/5.png", (720, 90))
        ship_4 = GameObject("data/4.png", (720, 190))
        ship_31 = GameObject("data/3.png", (720, 290))
        ship_32 = GameObject("data/3.png", (720, 390))
        ship_2 = GameObject("data/2.png", (720, 490))

        font = pygame.font.SysFont('agencyfb', 60, False, False)
        header_text = TextObject(font, "Place your fleet", (200, 12))
        footer_text = TextObject(font, "Press 'r' to rotate ship", (135, 600))
        ships_text = TextObject(font, "Your ships:", (720, 12))

        self.__texts = [header_text, footer_text, ships_text]
        self.__sprites = [background, board, ship_5, ship_4, ship_31, ship_32, ship_2]
        self.__ships = [ship_5, ship_4, ship_31, ship_32, ship_2]

        # todo: implement some kind of state, like selecting_ship, placing_ship etc

        loop = True
        dragging = False
        dragged_ship = None

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dragging = True
                        mouse_position = pygame.mouse.get_pos()
                        for ship in self.__ships:
                            if ship.rect.collidepoint(mouse_position):
                                dragged_ship = ship
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                        if dragged_ship:
                            if board.rect.collidepoint(dragged_ship.rect.topleft):
                                corner = dragged_ship.rect.topleft
                                pos_x = (corner[0] - 100) // 50
                                pos_y = (corner[1] - 90) // 50
                                mapped = (pos_x * 50 + 100, pos_y * 50 + 90)
                                dragged_ship.x, dragged_ship.y = mapped
                        dragged_ship = None
                elif event.type == pygame.MOUSEMOTION:
                    if dragging == 1 and dragged_ship:
                        mouse_position = pygame.mouse.get_pos()
                        dragged_ship.rect.center = mouse_position
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    if dragging == 1 and dragged_ship:
                        dragged_ship.rotate()
            self.__update_window()


if __name__ == "__main__":
    gui = GUI()
    gui.start()
