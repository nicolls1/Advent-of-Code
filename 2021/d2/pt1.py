SOURCE_FILE = 'numbers.txt'


def run():
  x = 0
  y = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      split = line.split(' ')
      direction = split[0]
      distance = int(split[1])

      if direction == 'forward':
        x += distance
      elif direction == 'up':
        y -= distance
      elif direction == 'down':
        y += distance
      else:
        raise 'Invalid direction'

  print(x * y)


if __name__ == '__main__':
  run()
