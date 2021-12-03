SOURCE_FILE = './numbers.txt'


def set_bits_from_list(l):
  val = 0b0
  for idx, entry in enumerate(l):
    val |= (entry << (len(l) - idx - 1))
  return val


def run():
  with open(SOURCE_FILE, 'r') as f:
    line = f.readline()
    counts = [[0, 0] for _ in line[:-1]]

  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      for idx, char in enumerate(line[:-1]):
        counts[idx][int(char)] += 1

  gamma = [0 if position[0] > position[1] else 1 for position in counts]
  epsilon = [0 if position[0] < position[1] else 1 for position in counts]

  int_gamma = set_bits_from_list(gamma)
  int_epsilon = set_bits_from_list(epsilon)

  print(int_gamma * int_epsilon)


if __name__ == '__main__':
  run()
