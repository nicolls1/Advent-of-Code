SOURCE_FILE = 'numbers.txt'

SELF_SCORES = {
  'A': 1,
  'B': 2,
  'C': 3
}

RESULT_SCORES = {
  'X': 0,
  'Y': 3,
  'Z': 6,
}

REQUIRED_RESPONSE = {
  'A': {
    'X': 'C',
    'Y': 'A',
    'Z': 'B',
  },
  'B': {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
  },
  'C': {
    'X': 'B',
    'Y': 'C',
    'Z': 'A',
  },
}


def run():
  total = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      split = line.split(' ')
      opponent = split[0].strip()
      result = split[1].strip()
      total += RESULT_SCORES[result] + SELF_SCORES[REQUIRED_RESPONSE[opponent][result]]

  print(total)


if __name__ == '__main__':
  run()
