
import pygame

from domain.ship import Ship


# class GameObject:
#
#     def __init__(self, image, position):
#         self._image = image
#         self._position = position
#
#     @property
#     def img(self):
#         return self._image
#
#     @property
#     def pos(self):
#         return self._position


# class GUIShip(pygame.sprite.Sprite, Ship):
#
#     def __init__(self, ship_id, image, position):
#         Ship.__init__(self, ship_id, position)
#         pygame.sprite.Sprite.__init__(self)


class GUI:

    def __init__(self):
        pass

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 680), pygame.SCALED)
        pygame.display.set_caption("Battleships")

        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((170, 238, 187))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    loop = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
        

if __name__ == "__main__":
    gui = GUI()
    gui.start()
