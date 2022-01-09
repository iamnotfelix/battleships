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
        self.__sprites = dict()
        self.__texts = dict()

        """ constants """
        self.BOARD_X = 200
        self.BOARD_Y = 90
        self.HEADER_X = 300
        self.HEADER_Y = 12
        self.FOOTER_X = 135  # 235
        self.FOOTER_Y = 600
        self.CONTENT_X = 820
        self.CONTENT_Y = 12
        self.FINISH_X = 680
        self.FINISH_Y = 600

        """ Screen state"""
        self.is_menu = False
        self.is_placing_ships = True
        self.is_playing = False

        """ States & active assets """
        self.loop = True
        self.dragging = False
        self.dragged_ship = None
        self.added_ships = list()

    def __update_window(self):
        for key in self.__sprites.keys():
            self.__screen.blit(self.__sprites[key].surface, self.__sprites[key].position)
        for key in self.__texts.keys():
            self.__screen.blit(self.__texts[key].surface, self.__texts[key].position)  # (200, 12)
        pygame.display.update()

    def __check_placed_ships(self):
        all_placed = True
        for ship in self.__ships:
            all_placed = all_placed and ship.placed
        return all_placed

    def __load_assets(self):
        background = GameObject("data/background.png", (0, 0))
        board = GameObject("data/board.png", (self.BOARD_X, self.BOARD_Y))
        ship_5 = GameObject("data/5.png", (820, 90), 5)
        ship_4 = GameObject("data/4.png", (820, 190), 4)
        ship_31 = GameObject("data/3.png", (820, 290), 3)
        ship_32 = GameObject("data/3.png", (820, 390), 3)
        ship_2 = GameObject("data/2.png", (820, 490), 2)

        font = pygame.font.SysFont('agencyfb', 60, False, False)
        header_text = TextObject(font, "Place your fleet", (self.HEADER_X, self.HEADER_Y))
        footer_text = TextObject(font, "Press 'R' to rotate ship", (self.FOOTER_X, self.FOOTER_Y))
        content_text = TextObject(font, "Your ships:", (self.CONTENT_X, self.CONTENT_Y))
        finish_text = TextObject(font, "Press 'Enter' when done", (self.FINISH_X, self.FINISH_Y))

        self.__texts = {
            "header": header_text,
            "footer": footer_text,
            "content": content_text,
            "finish": finish_text
        }
        self.__sprites = {
            "background" : background,
            "board": board,
            "ship_5": ship_5,
            "ship_4": ship_4,
            "ship_31": ship_31,
            "ship_32": ship_32,
            "ship_2": ship_2
        }
        self.__ships = [ship_5, ship_4, ship_31, ship_32, ship_2]

    def __ship_placing_screen(self, event):
        if event.type == pygame.QUIT:
            self.loop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                mouse_position = pygame.mouse.get_pos()
                for ship in self.__ships:
                    if ship.rect.collidepoint(mouse_position):
                        self.dragged_ship = ship
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                if self.dragged_ship:
                    if self.__sprites["board"].rect.collidepoint(self.dragged_ship.rect.topleft):
                        corner = self.dragged_ship.rect.topleft
                        pos_x = (corner[0] - self.BOARD_X) // 50
                        pos_y = (corner[1] - self.BOARD_Y) // 50
                        mapped = (pos_x * 50 + self.BOARD_X, pos_y * 50 + self.BOARD_Y)
                        self.dragged_ship.x, self.dragged_ship.y = mapped
                        self.dragged_ship.placed = True
                    else:
                        self.dragged_ship.placed = False
                self.dragged_ship = None
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging == 1 and self.dragged_ship:
                mouse_position = pygame.mouse.get_pos()
                self.dragged_ship.rect.center = mouse_position
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if self.dragging == 1 and self.dragged_ship:
                    self.dragged_ship.rotate()
            if event.key == pygame.K_RETURN:
                if self.__check_placed_ships():
                    try:
                        for ship in self.__ships:
                            if not (ship in self.added_ships):
                                ship_pos = ship.position
                                ship_pos = (
                                (ship_pos[0] - self.BOARD_X) // 50 + 1, (ship_pos[1] - self.BOARD_Y) // 50 + 1)
                                ship_pos = Position(ship_pos[1], ship_pos[0], ship.size, ship.orientation)
                                self.__player_logic.add_ship(ship_pos)
                                self.added_ships.append(ship)
                    except Exception as ex:
                        print(str(ex))
                        print("Not all ships are placed correctly!")
                    print("all")
                else:
                    print("Not all ships are placed correctly!")
        self.__update_window()

    def start(self):
        self.__load_assets()

        while self.loop:
            for event in pygame.event.get():
                if self.is_menu:
                    pass
                elif self.is_placing_ships:
                    self.__ship_placing_screen(event)
                elif self.is_playing:
                    pass


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
