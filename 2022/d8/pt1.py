from typing import Literal

SOURCE_FILE = 'numbers.txt'

DIRECTION_OFFSET = {
  'up': {
    'x': 0,
    'y': -1,
  },
  'right': {
    'x': 1,
    'y': 0,
  },
  'down': {
    'x': 0,
    'y': 1,
  },
  'left': {
    'x': -1,
    'y': 0,
  },
}


def is_out_of_bounds(pos: {'x': int, 'y': int}, width: int, height: int):
  return pos['x'] < 0 or pos['y'] < 0 or pos['x'] >= width or pos['y'] >= height


def find_board_for_direction(board: list[str], direction: Literal['up', 'down', 'left', 'right']):
  board_width = len(board[0])
  board_height = len(board)

  y_range = range(board_height) if direction != 'down' else range(board_height - 1, 0, -1)
  x_range = range(board_width) if direction != 'right' else range(board_width - 1, 0, -1)

  visible = [[False] * board_width for _ in range(board_height)]
  vertical = direction in ['up', 'down']
  max_heights = [0] * (board_width if vertical else board_height)

  for y in y_range:
    for x in x_range:
      compare_pos = {'x': x + DIRECTION_OFFSET[direction]['x'], 'y': y + DIRECTION_OFFSET[direction]['y']}
      max_pos = x if vertical else y
      if is_out_of_bounds(compare_pos, board_width, board_height) or (
          max_heights[max_pos] < int(board[y][x])
      ):
        max_heights[max_pos] = int(board[y][x])
        visible[y][x] = True
  return visible


def run():
  board = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      board.append(line.strip())

  grid_directions_visibility = {
    'up': find_board_for_direction(board, 'up'),
    'right': find_board_for_direction(board, 'right'),
    'down': find_board_for_direction(board, 'down'),
    'left': find_board_for_direction(board, 'left')
  }

  total_visibility = [
    [1 if (grid_directions_visibility['up'][y][x] or
           grid_directions_visibility['right'][y][x] or
           grid_directions_visibility['down'][y][x] or
           grid_directions_visibility['left'][y][x]) else 0
     for x in range(len(board[0]))] for y in range(len(board))
  ]
  print(sum([item for sublist in total_visibility for item in sublist]))


if __name__ == '__main__':
  run()
