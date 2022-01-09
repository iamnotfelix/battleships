import pygame

from gameObject import GameObject
from textObject import TextObject
from domain.position import Position
from validation.validation import PositionValidation


class MenuScreen:
    pass


class PlacingShipsScreen:

    def __init__(self, screen, player_logic):
        self.__player_logic = player_logic

        self.__screen = screen
        self.__ships = list()
        self.__sprites = dict()

        """ constants """
        self.BOARD_X = 200
        self.BOARD_Y = 90
        self.HEADER_X = 300
        self.HEADER_Y = 12
        self.PRESS_X = 100
        self.PRESS_Y = 600
        self.CONTENT_X = 820
        self.CONTENT_Y = 12

        """ States & active assets """
        self.loop = True
        self.dragging = False
        self.dragged_ship = None
        self.added_ships = list()

    def __update_window(self):
        for key in self.__sprites.keys():
            self.__screen.blit(self.__sprites[key].surface, self.__sprites[key].position)
        pygame.display.update()

    def __load_assets(self):
        background = GameObject("data/background.png", (0, 0))
        board = GameObject("data/board.png", (self.BOARD_X, self.BOARD_Y))
        ship_5 = GameObject("data/5.png", (820, 90), 5)
        ship_4 = GameObject("data/4.png", (820, 190), 4)
        ship_31 = GameObject("data/3.png", (820, 290), 3)
        ship_32 = GameObject("data/3.png", (820, 390), 3)
        ship_2 = GameObject("data/2.png", (820, 490), 2)

        font_header = pygame.font.SysFont('agencyfb', 60, False, False)
        font = pygame.font.SysFont("agencyfb", 50, False, False)
        header_text = TextObject(font_header, "Place your fleet", (self.HEADER_X, self.HEADER_Y))
        press_text = TextObject(font, "'R' - to rotate ship    'Enter' - to start playing     'Esc' - to go to menu",
                                (self.PRESS_X, self.PRESS_Y))
        content_text = TextObject(font, "Your ships:", (self.CONTENT_X, self.CONTENT_Y))

        self.__sprites = {
            "background": background,
            "board": board,
            "ship_5": ship_5,
            "ship_4": ship_4,
            "ship_31": ship_31,
            "ship_32": ship_32,
            "ship_2": ship_2,
            "header": header_text,
            "press": press_text,
            "content": content_text
        }
        self.__ships = [ship_5, ship_4, ship_31, ship_32, ship_2]

    def __check_placed_ships(self):
        all_placed = True
        for ship in self.__ships:
            all_placed = all_placed and ship.placed
        return all_placed

    def __event_handler(self, event):
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
                                ship_pos = ((ship_pos[0] - self.BOARD_X) // 50 + 1, (ship_pos[1] - self.BOARD_Y) // 50 + 1)
                                ship_pos = Position(ship_pos[1], ship_pos[0], ship.size, ship.orientation)
                                self.__player_logic.add_ship(ship_pos)
                                self.added_ships.append(ship)
                        return self.__ships
                        # todo: go to next screen
                    except Exception as ex:
                        print(str(ex))
                        # todo: create a pop up message for error
                        # todo: write on the same window a message (delete everything and write on background) for
                        #       an amount of time
                else:
                    # todo: same as above
                    print("Not all ships are placed correctly!")
        self.__update_window()
        return None

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                ships = self.__event_handler(event)
                if isinstance(ships, list):
                    return ships
                elif ships:
                    pass
                    # todo: go to menu option


class PlayingScreen:
    def __init__(self, screen, ships, player_logic, computer_logic):
        self.__player_logic = player_logic
        self.__computer_logic = computer_logic

        self.__screen = screen
        self.__ships = ships
        self.__sprites = dict()

        """ constants """
        self.BOARD_X = 90
        self.BOARD_Y = 100
        self.SHOTS_BOARD_X = 690
        self.SHOTS_BOARD_Y = 100
        self.HEADER1_X = 250
        self.HEADER1_Y = 12
        self.HEADER2_X = 830
        self.HEADER2_Y = 12
        self.PRESS_X = 480
        self.PRESS_Y = 600

        """ States & active assets """
        self.loop = True
        self.x_count = 1

    def __update_window(self):
        for key in self.__sprites.keys():
            self.__screen.blit(self.__sprites[key].surface, self.__sprites[key].position)
        pygame.display.update()

    def __set_ship_position(self):
        for ship in self.__ships:
            x, y = ship.position
            ship.x = x - 110
            ship.y = y + 10

    def __load_assets(self):
        background = GameObject("data/background.png", (0, 0))
        board = GameObject("data/board.png", (self.BOARD_X, self.BOARD_Y))
        shots_board = GameObject("data/board.png", (self.SHOTS_BOARD_X, self.SHOTS_BOARD_Y))

        font_header = pygame.font.SysFont('agencyfb', 60, False, False)
        font = pygame.font.SysFont("agencyfb", 50, False, False)
        header1_text = TextObject(font_header, "Your fleet", (self.HEADER1_X, self.HEADER1_Y))
        header2_text = TextObject(font_header, "Your shots", (self.HEADER2_X, self.HEADER2_Y))
        press_text = TextObject(font, "'Esc' - to go to menu", (self.PRESS_X, self.PRESS_Y))

        self.__set_ship_position()

        self.__sprites = {
            "background": background,
            "board": board,
            "shots_board": shots_board,
            "ship_5": self.__ships[0],
            "ship_4": self.__ships[1],
            "ship_31": self.__ships[2],
            "ship_32": self.__ships[3],
            "ship_2": self.__ships[4],
            "header1": header1_text,
            "header2": header2_text,
            "press": press_text
        }

    def __event_handler(self, event):
        if event.type == pygame.QUIT:
            self.loop = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.__sprites["shots_board"].rect.collidepoint(mouse_position):
                # player's turn
                coordinates = ((mouse_position[1] - 100) // 50 + 1, (mouse_position[0] - 690) // 50 + 1)
                coordinates = Position(coordinates[0], coordinates[1])
                self.__player_logic.record_hit(coordinates)
                is_hit, is_destroyed = self.__computer_logic.add_hit(coordinates)
                # todo: display a message to see if it hit or not

                # render player hit
                board_coordinates = ((coordinates.y - 1) * 50 + 690, (coordinates.x - 1) * 50 + 100)
                x_sprite = GameObject("data/x.png", board_coordinates)
                self.__sprites[f"x{self.x_count}"] = x_sprite
                self.x_count += 1

                # check if player wins
                if self.__computer_logic.is_game_over():
                    print("player wins")
                    # todo: make a pop up for player win, end the game and go to menu

                # computer turn
                computer_coordinates = self.__computer_logic.get_new_position()
                is_hit, is_destroyed = self.__player_logic.add_hit(computer_coordinates)
                self.__computer_logic.record_hit(computer_coordinates, is_hit, is_destroyed)

                # render computer hit
                computer_coordinates = ((computer_coordinates.y - 1) * 50 + 90, (computer_coordinates.x - 1) * 50 + 100)
                x_sprite = GameObject("data/x.png", computer_coordinates)
                self.__sprites[f"x{self.x_count}"] = x_sprite
                self.x_count += 1

                # check if computer wins
                if self.__player_logic.is_game_over():
                    print("computer wins")
                    # todo: make a pop up for computer win, end the game and go to the menu

        self.__update_window()

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                self.__event_handler(event)


class GUI:

    def __init__(self, player_logic, computer_logic):
        self.__player_logic = player_logic
        self.__computer_logic = computer_logic

        pygame.init()
        pygame.display.set_caption("Battleships")
        self.__screen = pygame.display.set_mode((1280, 680), pygame.SCALED)

        """ Screen state"""
        self.is_menu = False
        self.is_placing_ships = True
        self.is_playing = False

    def start(self):
        placing_screen = PlacingShipsScreen(self.__screen, self.__player_logic)
        ships = placing_screen.start()
        playing_screen = PlayingScreen(self.__screen, ships, player_logic, computer_logic)
        playing_screen.start()
        # while self.loop:
        #     for event in pygame.event.get():
        #         if self.is_menu:
        #             pass
        #         elif self.is_placing_ships:
        #             self.__ship_placing_screen(event)
        #         elif self.is_playing:
        #             pass


if __name__ == "__main__":
    from logic.logic import Logic
    from boards.board import Board
    from logic.computerLogic import ComputerLogic

    position_validator = PositionValidation()

    player_board = Board()
    player_shots_board = Board()

    computer_board = Board()
    computer_shots_board = Board()

    player_logic = Logic(player_board, player_shots_board, position_validator)
    computer_logic = ComputerLogic(computer_board, computer_shots_board, position_validator)
    computer_logic.init_board()
    # todo: init the board when it should be init-ed
    gui = GUI(player_logic, computer_logic)
    gui.start()
