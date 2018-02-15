import pygame
import sys
from pygame.locals import *
import config

assert config.menu_area_width >= 200, "Menu area must be at least 200 pixels wide"
assert config.play_area_width % config.cell_size == 0, "Play area width must be multiple of cell size"
assert config.play_area_height % config.cell_size == 0, "Play area height must be multiple of cell size"

button_list = []


def main():
    global fps_clock, display_surf, basic_font

    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((config.window_width, config.window_height))
    basic_font = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Game of Life')

    main_board = set()

    # Button surfaces and rectangles
    clear_surf, clear_rect, start_surf, start_rect, \
        ten_steps_surf, ten_steps_rect, step_surf, step_rect = create_button_objects()

    while True: # main game loop
        main_board = main_loop(main_board, clear_rect, start_rect, ten_steps_rect, step_rect)


def main_loop(main_board, clear_rect, start_rect, ten_steps_rect, step_rect):
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == MOUSEBUTTONUP:
            coordinates = click_spot(event.pos[0], event.pos[1])
            tick = 0
            # checks if user clicked menu button
            if coordinates is None:
                if clear_rect.collidepoint(event.pos):
                    main_board = set()
                if start_rect.collidepoint(event.pos):
                    while tick < 50:
                        main_board = reproduce(main_board, config.cell_row_quantity)
                        if not main_board:
                            break
                        tick += 1
                        draw_board(main_board)
                        pygame.display.update()
                        fps_clock.tick(config.FPS)
                if ten_steps_rect.collidepoint(event.pos):
                    while tick < 10:
                        main_board = reproduce(main_board, config.cell_row_quantity)
                        if not main_board:
                            break
                        tick += 1
                        draw_board(main_board)
                        pygame.display.update()
                        fps_clock.tick(config.FPS)
                if step_rect.collidepoint(event.pos):
                    main_board = reproduce(main_board, config.cell_row_quantity)
            else:
                check_and_flip(main_board, coordinates)
    draw_board(main_board)
    pygame.display.update()
    fps_clock.tick(config.FPS)
    return main_board


def neighbours(coordinates):
    x, y = coordinates
    neighbour_set = set()
    all_neighbours = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    ]
    for a, b in all_neighbours:
        neighbour_set.add((x + a, y + b))
    return neighbour_set


def reproduce(board, boardsize):
    next_gen_board = set()
    for cell_coordinates in board:
        neighbour_cells = neighbours(cell_coordinates)
        if len(board & neighbour_cells) in (2, 3):
            next_gen_board.add(cell_coordinates)
        for n in neighbour_cells:
            if len(board & neighbours(n)) == 3 \
                    and boardsize > n[0] >= 0 \
                    and boardsize > n[1] >= 0:
                next_gen_board.add(n)

    return next_gen_board


def terminate():
    pygame.quit()
    sys.exit()


def check_and_flip(board, coordinates):
    if coordinates in board:
        board.remove(coordinates)
    else:
        board.add(coordinates)


def create_button_objects():
    clear_surf, clear_rect = make_text(
        'Clear Board', config.text_color, config.text_bg_color,
        config.play_area_width + 10, config.button_pos_vertical * 4
    )
    start_surf, start_rect = make_text(
        '50 Generations', config.text_color, config.text_bg_color,
        config.play_area_width + 10, config.button_pos_vertical
    )
    ten_steps_surf, ten_steps_rect = make_text(
        '10 Generations', config.text_color, config.text_bg_color,
        config.play_area_width + 10, config.button_pos_vertical * 2
    )
    step_surf, step_rect = make_text(
        'One Generation Step', config.text_color, config.text_bg_color,
        config.play_area_width + 10, config.button_pos_vertical * 3
    )
    return clear_surf, clear_rect, start_surf, start_rect, \
        ten_steps_surf, ten_steps_rect, step_surf, step_rect


def get_left_top_of_cell(x, y):
    left = x * config.cell_size
    top = y * config.cell_size
    return left, top


def click_spot(event_pos_x, event_pos_y):
    for x in range(config.cell_row_quantity):
        for y in range(config.cell_column_quantity):
            left, top = get_left_top_of_cell(x, y)
            cell_rect = pygame.Rect(left, top, config.cell_size, config.cell_size)
            if cell_rect.collidepoint(event_pos_x, event_pos_y):
                return x, y


def make_text(text, color, bgcolor, top, left):
    text_surf = basic_font.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    button_list.append((text_surf, text_rect))
    return text_surf, text_rect


def draw_board(board):
    display_surf.fill(config.BLACK)
    for cell in board:
        draw_cell(cell)
    for surf_rect_pair in button_list:
        draw_button(surf_rect_pair[0], surf_rect_pair[1])
    draw_grid()


def draw_button(surf, rect):
    display_surf.blit(surf, rect)


def draw_cell(cell):
    left, top = get_left_top_of_cell(cell[0], cell[1])
    pygame.draw.rect(display_surf, config.WHITE, (left, top, config.cell_size, config.cell_size))


def draw_grid():
    for x in range(0, config.play_area_width + config.cell_size, config.cell_size):
        pygame.draw.line(display_surf, config.LIGHTBLUE, (x, 0), (x, config.play_area_height))
    for y in range(0, config.window_height, config.cell_size):
        pygame.draw.line(display_surf, config.LIGHTBLUE, (0, y), (config.play_area_width, y))


if __name__ == '__main__':
    main()
