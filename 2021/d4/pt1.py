from collections import defaultdict

SOURCE_FILE = 'numbers.txt'

# Assign each position a number
#  0  1  2  3  4
#  5  6  7  8  9
# 10 11 12 13 14
# 15 16 17 18 19
# 20 21 22 23 24

WINNING_COMBINATIONS = [
  # Horizontal
  {0, 1, 2, 3, 4},
  {5, 6, 7, 8, 9},
  {10, 11, 12, 13, 14},
  {15, 16, 17, 18, 19},
  {20, 21, 22, 23, 24},
  # Vertical
  {0, 5, 10, 15, 20},
  {1, 6, 11, 16, 21},
  {2, 7, 12, 17, 22},
  {3, 8, 13, 18, 23},
  {4, 9, 14, 19, 24},
]


def board_has_winning_combination(board_found_positions):
  for combo in WINNING_COMBINATIONS:
    if combo <= set(board_found_positions):
      return True
  return False


def run():
  boards = []
  with open(SOURCE_FILE, 'r') as f:
    input_numbers = [int(num) for num in f.readline().strip().split(',')]
    f.readline()

    boards_buffer = []
    for line in f:
      if len(line) == 1:
        boards.append(boards_buffer)
        boards_buffer = []
        continue

      row = list(filter(lambda entry: len(entry) > 0, line.strip().split(' ')))
      for value in row:
        boards_buffer.append(int(value))

    if len(boards_buffer) > 0:
      boards.append(boards_buffer)

  board_found_number_positions = [[] for _ in boards]
  numbers_to_boards_position_map = defaultdict(list)
  for idx, board in enumerate(boards):
    for jdx, number in enumerate(board):
      numbers_to_boards_position_map[number].append((idx, jdx))

  for number in input_numbers:
    # pick next number
    boards_with_number = numbers_to_boards_position_map[number]
    for board in boards_with_number:
      board_found_number_positions[board[0]].append(board[1])

    # check for winners
    for idx, board in enumerate(board_found_number_positions):
      if board_has_winning_combination(board):
        winning_board = boards[idx]
        for position in board:
          winning_board[position] = 0
        remaining_numbers_sum = sum(winning_board)
        print(number * remaining_numbers_sum)
        return


if __name__ == '__main__':
  run()
