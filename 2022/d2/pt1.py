SOURCE_FILE = 'numbers.txt'

SELF_SCORES = {
  'X': 1,
  'Y': 2,
  'Z': 3
}

RESULT_SCORES = {
  'A': {
    'X': 3,
    'Y': 6,
    'Z': 0,
  },
  'B': {
    'X': 0,
    'Y': 3,
    'Z': 6,
  },
  'C': {
    'X': 6,
    'Y': 0,
    'Z': 3,
  }
}


def run():
  total = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      split = line.split(' ')
      opponent = split[0].strip()
      self = split[1].strip()
      total += SELF_SCORES[self] + RESULT_SCORES[opponent][self]

  print(total)


if __name__ == '__main__':
  run()
