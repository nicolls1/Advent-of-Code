SOURCE_FILE = 'numbers.txt'


# is range2 inside range1
def is_inside(range1, range2):
  return range1[0] <= range2[0] and range1[1] >= range2[1]


def run():
  count = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      first, second = line.strip().split(',')
      first_range = [int(number) for number in first.split('-')]
      second_range = [int(number) for number in second.split('-')]

      if is_inside(first_range, second_range) or is_inside(second_range, first_range):
        count += 1

  print(count)


if __name__ == '__main__':
  run()
