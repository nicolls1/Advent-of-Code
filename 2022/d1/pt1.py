SOURCE_FILE = 'numbers.txt'


def run():
  sums = [0]
  current_index = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      if line == '\n':
        sums.append(0)
        current_index += 1
        continue
      num = int(line)
      sums[current_index] += num

  print(max(sums))


if __name__ == '__main__':
  run()
