# -*- coding: utf-8 -*-

FPS = 10
window_width = 1000
window_height = 800
cell_size = 10
menu_area_width = window_width - window_height
play_area_width = window_width - menu_area_width
play_area_height = window_height
cell_width = int(play_area_width / cell_size)
cell_height = int(play_area_height / cell_size)
cell_row_quantity = int(play_area_width / cell_size)
cell_column_quantity = int(play_area_height / cell_size)
button_pos_vertical = 25
# Colors used, R G B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (20, 30, 50)
grid_color = LIGHTBLUE
text_bg_color = BLACK
text_color = WHITE