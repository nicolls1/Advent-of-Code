SOURCE_FILE = './numbers.txt'


def run():
  count = 0
  prev = None
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      num = int(line)
      if prev is None:
        prev = num
        continue
      if num > prev:
        count += 1
      prev = num

  print(count)


if __name__ == '__main__':
  run()
