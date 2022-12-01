import math

SOURCE_FILE = 'numbers.txt'


def is_inside(dimensions, x, y):
  return dimensions['width'] > x >= 0 and dimensions['height'] > y >= 0


def get_neighbors(data, dimensions, x, y):
  return {
    'top': {'value': data[y - 1][x], 'x': x, 'y': y - 1} if is_inside(dimensions, x, y - 1) else None,
    'right': {'value': data[y][x + 1], 'x': x + 1, 'y': y} if is_inside(dimensions, x + 1, y) else None,
    'bottom': {'value': data[y + 1][x], 'x': x, 'y': y + 1} if is_inside(dimensions, x, y + 1) else None,
    'left': {'value': data[y][x - 1], 'x': x - 1, 'y': y} if is_inside(dimensions, x - 1, y) else None,
  }


def get_point_key(point):
  return ','.join([str(p) for p in point])


def get_basin(data, dimensions, low_point):
  visited = set()
  active_points = [low_point]

  while len(active_points) > 0:
    active_point = active_points.pop()
    visited.add(get_point_key(active_point))

    for neighbor in get_neighbors(data, dimensions, active_point[0], active_point[1]).values():
      if neighbor is not None and \
          get_point_key([neighbor['x'], neighbor['y']]) not in visited and \
          neighbor['value'] < 9:
        active_points.append([neighbor['x'], neighbor['y']])
  return visited


def run():
  data = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      data.append([int(c) for c in line.strip()])

  dimensions = {
    'width': len(data[0]),
    'height': len(data),
  }

  low_points = []
  for y, line in enumerate(data):
    for x, value in enumerate(line):
      neighbors = get_neighbors(data, dimensions, x, y)
      if all(neighbor['value'] > value if neighbor is not None else True for neighbor in neighbors.values()):
        low_points.append([x, y])

  basins = []
  for low_point in low_points:
    basins.append(get_basin(data, dimensions, low_point))

  basin_lengths = [len(basin) for basin in basins]
  basin_lengths.sort(reverse=True)
  print(math.prod(basin_lengths[:3]))


if __name__ == '__main__':
  run()
