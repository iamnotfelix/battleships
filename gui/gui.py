import pygame

from gameObject import GameObject
from textObject import TextObject
from domain.position import Position
from validation.validation import PositionValidation


class State:

    def __init__(self):
        self.dragging = False
        self.ship_dragged = None


class GUI:

    def __init__(self, player_logic, computer_logic):
        self.__player_logic = player_logic
        self.__computer_logic = computer_logic

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
            self.__screen.blit(text.surface, text.position)  # (200, 12)
        pygame.display.update()

    def __check_placed_ships(self):
        all_placed = True
        for ship in self.__ships:
            all_placed = all_placed and ship.placed
        return all_placed

    def start(self):

        BOARD_X = 200
        BOARD_Y = 90
        HEADER_X = 300
        HEADER_Y = 12
        FOOTER_X = 135  # 235
        FOOTER_Y = 600
        CONTENT_X = 820
        CONTENT_Y = 12
        FINISH_X = 680
        FINISH_Y = 600

        background = GameObject("data/background.png", (0, 0))
        board = GameObject("data/board.png", (BOARD_X, BOARD_Y))
        ship_5 = GameObject("data/5.png", (820, 90), 5)
        ship_4 = GameObject("data/4.png", (820, 190), 4)
        ship_31 = GameObject("data/3.png", (820, 290), 3)
        ship_32 = GameObject("data/3.png", (820, 390), 3)
        ship_2 = GameObject("data/2.png", (820, 490), 2)

        font = pygame.font.SysFont('agencyfb', 60, False, False)
        header_text = TextObject(font, "Place your fleet", (HEADER_X, HEADER_Y))
        footer_text = TextObject(font, "Press 'R' to rotate ship", (FOOTER_X, FOOTER_Y))
        content_text = TextObject(font, "Your ships:", (CONTENT_X, CONTENT_Y))
        finish_text = TextObject(font, "Press 'Enter' when done", (FINISH_X, FINISH_Y))

        self.__texts = [header_text, footer_text, content_text, finish_text]
        self.__sprites = [background, board, ship_5, ship_4, ship_31, ship_32, ship_2]
        self.__ships = [ship_5, ship_4, ship_31, ship_32, ship_2]

        loop = True
        dragging = False
        dragged_ship = None
        added_ships = list()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                                pos_x = (corner[0] - BOARD_X) // 50
                                pos_y = (corner[1] - BOARD_Y) // 50
                                mapped = (pos_x * 50 + BOARD_X, pos_y * 50 + BOARD_Y)
                                dragged_ship.x, dragged_ship.y = mapped
                                dragged_ship.placed = True
                            else:
                                dragged_ship.placed = False
                        dragged_ship = None
                elif event.type == pygame.MOUSEMOTION:
                    if dragging == 1 and dragged_ship:
                        mouse_position = pygame.mouse.get_pos()
                        dragged_ship.rect.center = mouse_position
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if dragging == 1 and dragged_ship:
                            dragged_ship.rotate()
                    if event.key == pygame.K_RETURN:
                        if self.__check_placed_ships():
                            try:
                                for ship in self.__ships:
                                    if not (ship in added_ships):
                                        ship_pos = ship.position
                                        ship_pos = ((ship_pos[0] - BOARD_X) // 50 + 1, (ship_pos[1] - BOARD_Y) // 50 + 1)
                                        ship_pos = Position(ship_pos[1], ship_pos[0], ship.size, ship.orientation)
                                        self.__player_logic.add_ship(ship_pos)
                                        print("asdfasdfasdf")
                                        added_ships.append(ship)
                            except Exception as ex:
                                print(str(ex))
                                print("Not all ships are placed correctly!")
                            print("all")
                        else:
                            print("Not all ships are placed correctly!")
            self.__update_window()


if __name__ == "__main__":
    from logic.logic import Logic
    from boards.board import Board

    position_validator = PositionValidation()

    player_board = Board()
    player_shots_board = Board()

    computer_board = Board()
    computer_shots_board = Board()

    player_logic = Logic(player_board, player_shots_board, position_validator)
    computer_logic = Logic(computer_board, computer_shots_board, position_validator)
    gui = GUI(player_logic, computer_logic)
    gui.start()
