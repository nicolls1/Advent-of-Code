import math

SOURCE_FILE = 'numbers.txt'


def move_cost(length):
  return 0.5 * length * (length + 1)


def sum_move_cost(positions, average):
  return sum([move_cost(abs(position - average)) for position in positions])


def run():
  with open(SOURCE_FILE, 'r') as f:
    positions = [int(pos) for pos in f.readline().strip().split(',')]

  average = sum(positions) / len(positions)
  print(min(sum_move_cost(positions, math.floor(average)), sum_move_cost(positions, math.ceil(average))))


if __name__ == '__main__':
  run()
