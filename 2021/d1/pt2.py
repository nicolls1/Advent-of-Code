import collections

SOURCE_FILE = 'numbers.txt'


def run():
  count = 0
  buffer = collections.deque(maxlen=3)
  prev = None
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      num = int(line)
      if len(buffer) < 3:
        buffer.append(num)
        prev = sum(buffer)
        continue
      buffer.append(num)
      print(sum(buffer))
      if sum(buffer) > prev:
        count += 1
      prev = sum(buffer)

  print(count)


if __name__ == '__main__':
  run()
