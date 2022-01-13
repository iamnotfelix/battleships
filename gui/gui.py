import sys
import pygame

from gui.gameObject import GameObject
from gui.textObject import TextObject

from domain.position import Position

from validation.validation import PositionValidation
from logic.logic import Logic
from boards.board import Board
from logic.computerLogic import ComputerLogic


class MenuScreen:

    def __init__(self, screen):
        self.__screen = screen
        self.__sprites = dict()

        self.loop = True
        self.sys_cursor = pygame.mouse.get_cursor()

        self.TITLE_X = 440
        self.TITLE_Y = 100
        self.PLAY_X = 440
        self.PLAY_Y = 280
        self.EXIT_X = 440
        self.EXIT_Y = 400

    def __update_window(self):
        for key in self.__sprites.keys():
            self.__screen.blit(self.__sprites[key].surface, self.__sprites[key].position)
        pygame.display.update()

    def __load_assets(self):
        background = GameObject("gui/data/background.png", (0, 0))

        font_title = pygame.font.SysFont('agencyfb', 115, False, False)
        title_text = TextObject(font_title, "Battleships", (self.TITLE_X, self.TITLE_Y))

        play_button = GameObject("gui/data/play.png", (self.PLAY_X, self.PLAY_Y))
        exit_button = GameObject("gui/data/exit.png", (self.EXIT_X, self.EXIT_Y))

        self.__sprites = {
            "background": background,
            "title": title_text,
            "play": play_button,
            "exit": exit_button
        }

    def __event_handler(self, event):
        if event.type == pygame.QUIT:
            self.loop = False
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            if self.__sprites["play"].rect.collidepoint(mouse_position) or \
                    self.__sprites["exit"].rect.collidepoint(mouse_position):
                pygame.mouse.set_cursor(pygame.cursors.diamond)
            else:
                pygame.mouse.set_cursor(self.sys_cursor)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.__sprites["play"].rect.collidepoint(mouse_position):
                btn_pos = self.__sprites["play"].position
                active_button = GameObject("gui/data/play_active.png", btn_pos)
                self.__sprites["play"] = active_button
            elif self.__sprites["exit"].rect.collidepoint(mouse_position):
                btn_pos = self.__sprites["exit"].position
                active_button = GameObject("gui/data/exit_active.png", btn_pos)
                self.__sprites["exit"] = active_button
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            if self.__sprites["play"].rect.collidepoint(mouse_position):
                pygame.mouse.set_cursor(self.sys_cursor)
                self.loop = False
            elif self.__sprites["exit"].rect.collidepoint(mouse_position):
                self.loop = False
                sys.exit()
            else:
                self.__sprites["play"] = GameObject("gui/data/play.png", self.__sprites["play"].position)
                self.__sprites["exit"] = GameObject("gui/data/exit.png", self.__sprites["exit"].position)
        self.__update_window()

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                self.__event_handler(event)


class InfoScreen:

    def __init__(self, screen, text):
        self.__screen = screen
        self.__main_text = text
        self.__sprites = dict()

        """ Constants """
        self.MAIN_X = None
        self.MAIN_Y = None
        self.PRESS_X = 480
        self.PRESS_Y = 600

        """ States """
        self.loop = True

    def __update_window(self):
        for key in self.__sprites.keys():
            self.__screen.blit(self.__sprites[key].surface, self.__sprites[key].position)
        pygame.display.update()

    def __get_text_offset(self, font):
        text_rect = font.render(self.__main_text, True, (0, 0, 0)).get_rect()
        offset = (text_rect.width // 2, text_rect.height // 2)
        return offset

    def __load_assets(self):
        background = GameObject("gui/data/background.png", (0, 0))

        font_main = pygame.font.SysFont('agencyfb', 60, False, False)
        offset = self.__get_text_offset(font_main)
        self.MAIN_X = self.__screen.get_rect().center[0] - offset[0]
        self.MAIN_Y = self.__screen.get_rect().center[1] - offset[1]
        main_text = TextObject(font_main, self.__main_text, (self.MAIN_X, self.MAIN_Y))

        font = pygame.font.SysFont("agencyfb", 50, False, False)
        press_text = TextObject(font, "'Enter' - to continue", (self.PRESS_X, self.PRESS_Y))

        self.__sprites = {
            "background": background,
            "press": press_text,
            "main": main_text
        }

    def __event_handler(self, event):
        if event.type == pygame.QUIT:
            self.loop = False
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.loop = False
        self.__update_window()

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                self.__event_handler(event)


class PlacingShipsScreen:

    def __init__(self, screen, player_logic):
        self.__player_logic = player_logic

        self.__screen = screen
        self.__ships = list()
        self.__sprites = dict()

        """ Constants """
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
        background = GameObject("gui/data/background.png", (0, 0))
        board = GameObject("gui/data/board.png", (self.BOARD_X, self.BOARD_Y))
        ship_5 = GameObject("gui/data/5.png", (820, 90), 5)
        ship_4 = GameObject("gui/data/4.png", (820, 190), 4)
        ship_31 = GameObject("gui/data/3.png", (820, 290), 3)
        ship_32 = GameObject("gui/data/3.png", (820, 390), 3)
        ship_2 = GameObject("gui/data/2.png", (820, 490), 2)

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
            sys.exit()
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
            if self.dragging == 1 and self.dragged_ship and not (self.dragged_ship in self.added_ships):
                mouse_position = pygame.mouse.get_pos()
                self.dragged_ship.rect.center = mouse_position
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.loop = False
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
                    except Exception as ex:
                        info_screen = InfoScreen(self.__screen, str(ex))
                        info_screen.start()
                else:
                    info_screen = InfoScreen(self.__screen, "Not all ships are placed correctly!")
                    info_screen.start()
        self.__update_window()
        return None

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                ships = self.__event_handler(event)
                if isinstance(ships, list):
                    return ships


class PlayingScreen:
    def __init__(self, screen, ships, player_logic, computer_logic):
        self.__player_logic = player_logic
        self.__computer_logic = computer_logic

        self.__screen = screen
        self.__ships = ships
        self.__sprites = dict()

        """ Constants """
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
        background = GameObject("gui/data/background.png", (0, 0))
        board = GameObject("gui/data/board.png", (self.BOARD_X, self.BOARD_Y))
        shots_board = GameObject("gui/data/board.png", (self.SHOTS_BOARD_X, self.SHOTS_BOARD_Y))

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
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.__sprites["shots_board"].rect.collidepoint(mouse_position):
                # player's turn
                coordinates = ((mouse_position[1] - 100) // 50 + 1, (mouse_position[0] - 690) // 50 + 1)
                coordinates = Position(coordinates[0], coordinates[1])
                self.__player_logic.record_hit(coordinates)
                is_hit, is_destroyed = self.__computer_logic.add_hit(coordinates)

                # render player hit
                board_coordinates = ((coordinates.y - 1) * 50 + 690, (coordinates.x - 1) * 50 + 100)
                if is_hit:
                    hit_part = GameObject("gui/data/1.png", board_coordinates)
                    self.__sprites[f"x{self.x_count}"] = hit_part
                    self.x_count += 1
                x_sprite = GameObject("gui/data/x.png", board_coordinates)
                self.__sprites[f"x{self.x_count}"] = x_sprite
                self.x_count += 1
                if is_destroyed:
                    info_screen = InfoScreen(self.__screen, "You destroyed a ship!")
                    info_screen.start()

                # check if player wins
                if self.__computer_logic.is_game_over():
                    print("player wins")
                    info_screen = InfoScreen(self.__screen, "You won! GGEZ <33333")
                    info_screen.start()
                    self.loop = False

                # computer turn
                computer_coordinates = self.__computer_logic.get_new_position()
                is_hit, is_destroyed = self.__player_logic.add_hit(computer_coordinates)
                self.__computer_logic.record_hit(computer_coordinates, is_hit, is_destroyed)

                # render computer hit
                computer_coordinates = ((computer_coordinates.y - 1) * 50 + 90, (computer_coordinates.x - 1) * 50 + 100)
                x_sprite = GameObject("gui/data/x.png", computer_coordinates)
                self.__sprites[f"x{self.x_count}"] = x_sprite
                self.x_count += 1

                # check if computer wins
                if self.__player_logic.is_game_over():
                    print("computer wins")
                    info_screen = InfoScreen(self.__screen, "You lost! XD")
                    info_screen.start()
                    self.loop = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.loop = False
        self.__update_window()

    def start(self):
        self.__load_assets()
        while self.loop:
            for event in pygame.event.get():
                self.__event_handler(event)


class GUI:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Battleships")
        self.__screen = pygame.display.set_mode((1280, 680), pygame.SCALED)

        """ Screen state"""
        self.loop = True
        self.is_menu = False
        self.is_placing_ships = True
        self.is_playing = False

    @staticmethod
    def __get_new_player():
        position_validator = PositionValidation()
        player_board = Board()
        player_shots_board = Board()

        return Logic(player_board, player_shots_board, position_validator)

    @staticmethod
    def __get_new_computer():
        position_validator = PositionValidation()
        computer_board = Board()
        computer_shots_board = Board()

        computer_logic = ComputerLogic(computer_board, computer_shots_board, position_validator)
        computer_logic.init_board()
        return computer_logic

    def start(self):
        while True:
            menu_screen = MenuScreen(self.__screen)
            menu_screen.start()
            player_logic = self.__get_new_player()
            placing_screen = PlacingShipsScreen(self.__screen, player_logic)
            ships = placing_screen.start()
            if ships:
                computer_logic = self.__get_new_computer()
                playing_screen = PlayingScreen(self.__screen, ships, player_logic, computer_logic)
                playing_screen.start()
