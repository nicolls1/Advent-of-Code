SOURCE_FILE = 'numbers.txt'

OFFSETS = {
  'up': [0, 1, 0],
  'down': [0, -1, 0],
  'left': [-1, 0, 0],
  'right': [1, 0, 0],
  'front': [0, 0, 1],
  'back': [0, 0, -1],
}


def position_to_string(point: list[int]):
  return ','.join([str(dim) for dim in point])


class Point:
  def __init__(self, position: list[int], up: 'Point' = None, down: 'Point' = None, left: 'Point' = None,
               right: 'Point' = None, front: 'Point' = None,
               back: 'Point' = None):
    self.position = position
    self.up = up
    self.down = down
    self.left = left
    self.right = right
    self.front = front
    self.back = back

  def get_open_count(self):
    count = 0
    for direction in OFFSETS.keys():
      if getattr(self, direction) is None:
        count += 1
    return count

  def __str__(self):
    return f'{position_to_string(self.position)}: {"^" if self.up is not None else "."}' + \
           f'{"v" if self.down is not None else "."}' + \
           f'{"<" if self.left is not None else "."}' + \
           f'{">" if self.right is not None else "."}' + \
           f'{"f" if self.down is not None else "."}' + \
           f'{"b" if self.back is not None else "."}'


def add_positions(p1, p2):
  return [a + b for a, b in zip(p1, p2)]


def run():
  points = {}
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      str_point = line.strip()
      points[str_point] = Point([int(dim) for dim in str_point.split(',')])

  for point in points.values():
    for direction, offset in OFFSETS.items():
      neighbor = add_positions(point.position, offset)
      neighbor_string = position_to_string(neighbor)
      if neighbor_string in points:
        setattr(point, direction, points[neighbor_string])

  counts = [point.get_open_count() for point in points.values()]
  print(sum(counts))


if __name__ == '__main__':
  run()
