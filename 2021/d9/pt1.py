SOURCE_FILE = 'numbers.txt'


def inside(dimensions, x, y):
  return dimensions['width'] > x >= 0 and dimensions['height'] > y >= 0


def run():
  data = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      data.append([int(c) for c in line.strip()])

  dimensions = {
    'width': len(data[0]),
    'height': len(data),
  }

  risk_level_sum = 0
  for y, line in enumerate(data):
    for x, value in enumerate(line):
      trbl = {
        'top': data[y - 1][x] if inside(dimensions, x, y - 1) else None,
        'right': data[y][x + 1] if inside(dimensions, x + 1, y) else None,
        'bottom': data[y + 1][x] if inside(dimensions, x, y + 1) else None,
        'left': data[y][x - 1] if inside(dimensions, x - 1, y) else None,
      }

      if all(neighbor > value if neighbor is not None else True for neighbor in trbl.values()):
        risk_level_sum += value + 1
  print(risk_level_sum)


if __name__ == '__main__':
  run()
