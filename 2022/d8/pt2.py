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


def get_next_position(pos: {'x': int, 'y': int}, direction: Literal['up', 'down', 'left', 'right']):
  return {'x': pos['x'] + DIRECTION_OFFSET[direction]['x'], 'y': pos['y'] + DIRECTION_OFFSET[direction]['y']}


def get_position_value(board, pos: {'x': int, 'y': int}):
  return board[pos['y']][pos['x']]


def count_direction_visibility(board, direction: Literal['up', 'down', 'left', 'right'], pos: {'x': int, 'y': int}):
  count = 0
  start_height = get_position_value(board, pos)
  current_pos = pos

  while True:
    next_position = get_next_position(current_pos, direction)
    if is_out_of_bounds(next_position, len(board[0]), len(board)):
      return count

    next_height = get_position_value(board, next_position)
    if next_height >= start_height:
      return count + 1
    count += 1
    current_pos = next_position


def find_board_for_direction(board: list[str], direction: Literal['up', 'down', 'left', 'right']):
  board_width = len(board[0])
  board_height = len(board)
  visible = [[0] * board_width for _ in range(board_height)]

  for y in range(board_height):
    for x in range(board_width):
      current_pos = {'x': x, 'y': y}
      visible[y][x] = count_direction_visibility(board, direction, current_pos)
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

  visibility_scores = [
    [grid_directions_visibility['up'][y][x] *
     grid_directions_visibility['right'][y][x] *
     grid_directions_visibility['down'][y][x] *
     grid_directions_visibility['left'][y][x]
     for x in range(len(board[0]))] for y in range(len(board))
  ]
  print(max([item for sublist in visibility_scores for item in sublist]))


if __name__ == '__main__':
  run()
