import statistics

SOURCE_FILE = './numbers.txt'


def run():
  with open(SOURCE_FILE, 'r') as f:
    positions = [int(pos) for pos in f.readline().strip().split(',')]

  median = statistics.median(positions)
  print(sum([abs(position - median) for position in positions]))


if __name__ == '__main__':
  run()
