SOURCE_FILE = 'numbers.txt'


def overlap(range1, range2):
  return range1[1] >= range2[0] and range1[1] <= range2[1] or range2[1] >= range1[0] and range2[1] <= range1[1]


def run():
  count = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      first, second = line.strip().split(',')
      first_range = [int(number) for number in first.split('-')]
      second_range = [int(number) for number in second.split('-')]

      if overlap(first_range, second_range):
        count += 1

  print(count)


if __name__ == '__main__':
  run()
