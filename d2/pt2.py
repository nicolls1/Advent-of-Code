SOURCE_FILE = './numbers.txt'


def run():
  aim = 0
  x = 0
  y = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      split = line.split(' ')
      direction = split[0]
      distance = int(split[1])

      if direction == 'forward':
        x += distance
        y += distance * aim
      elif direction == 'up':
        aim -= distance
      elif direction == 'down':
        aim += distance
      else:
        raise 'Invalid direction'

  print(x * y)


if __name__ == '__main__':
  run()
