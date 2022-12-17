import math

SOURCE_FILE = 'numbers.txt'
END_ROCKS = 2022
ROW_WIDTH = 7
NEW_ROCK_OFFSET = 3
DOWN = 'v'
LEFT = '<'
RIGHT = '>'

ROCKS = [
  {
    'points': [[0, 0], [1, 0], [2, 0], [3, 0]],
    'height': 1,
  },
  {
    'points': [[1, 0], [0, -1], [1, -1], [2, -1], [1, -2]],
    'height': 3,
  },
  {
    'points': [[2, 0], [2, -1], [0, -2], [1, -2], [2, -2]],
    'height': 3
  },
  {
    'points': [[0, 0], [0, -1], [0, -2], [0, -3]],
    'height': 4

  },
  {
    'points': [[0, 0], [1, 0], [0, -1], [1, -1]],
    'height': 2
  }
]


def get_move_direction_for_time(jets: str, time: int):
  if time % 2 == 1:
    return DOWN
  return jets[math.floor(time / 2) % len(jets)]


def print_board(board: list[list[bool]]):
  for row in board[::-1]:
    print(row)


def board_row():
  return [False] * ROW_WIDTH


def find_top_rock(board: list[list[bool]]):
  for i, row in enumerate(board[::-1]):
    for place in row:
      if place:
        return len(board) - 1 - i
  return -1


DIRECTION_OFFSETS = {
  DOWN: [0, -1],
  LEFT: [-1, 0],
  RIGHT: [1, 0],
}


def add_points(p1, p2):
  return [a + b for a, b in zip(p1, p2)]


def is_position_open(board: list[list[bool]], position: list[int]):
  return 0 <= position[0] <= ROW_WIDTH - 1 and 0 <= position[1] <= len(board) - 1 and not board[position[1]][
    position[0]]


def can_rock_move(board: list[list[bool]], rock_root: list[int], rock: list[list[int]],
                  direction: str):
  test_root = add_points(rock_root, DIRECTION_OFFSETS[direction])
  for position in rock:
    if not is_position_open(board, add_points(test_root, position)):
      return False
  return True


def add_rock_to_board(board: list[list[bool]], rock_root_offset: list[int], rock: list[list[int]]):
  for rock_position in rock:
    board_position = add_points(rock_root_offset, rock_position)
    board[board_position[1]][board_position[0]] = True


def run():
  with open(SOURCE_FILE, 'r') as f:
    jets = f.readline().strip()
  rock_count = 0

  board = [board_row()]
  time = 0

  while rock_count < END_ROCKS:
    top_rock = find_top_rock(board)

    if top_rock + 1 + NEW_ROCK_OFFSET + ROCKS[rock_count % len(ROCKS)]['height'] - len(board) >= 0:
      for _ in range(top_rock + 1 + NEW_ROCK_OFFSET + ROCKS[rock_count % len(ROCKS)]['height'] - len(board)):
        board.append(board_row())
    else:
      for _ in range(abs(top_rock + 1 + NEW_ROCK_OFFSET + ROCKS[rock_count % len(ROCKS)]['height'] - len(board))):
        board.pop()

    rock = ROCKS[rock_count % len(ROCKS)]['points']
    rock_root_offset = [2, len(board) - 1]

    while True:
      move_direction = get_move_direction_for_time(jets, time)
      can_move = can_rock_move(board, rock_root_offset, rock, move_direction)
      if not can_move and move_direction == DOWN:
        time += 1
        break
      if can_move:
        rock_root_offset = add_points(rock_root_offset, DIRECTION_OFFSETS[move_direction])

      time += 1

    add_rock_to_board(board, rock_root_offset, rock)
    rock_count += 1

  print(find_top_rock(board) + 1)


if __name__ == '__main__':
  run()
