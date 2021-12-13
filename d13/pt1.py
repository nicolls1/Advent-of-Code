SOURCE_FILE = 'numbers.txt'


def empty_grid(dimensions):
  return [[False] * dimensions['width'] for _ in range(dimensions['height'])]


def fold_x(grid, dimensions, offset):
  new_dimensions = {
    'width': max(offset, dimensions['width'] - offset - 1),
    'height': dimensions['height'],
  }
  new_grid = empty_grid(new_dimensions)
  for y, line in enumerate(grid):
    for x, value in enumerate(line):
      if x < offset:
        new_grid[y][x] = value
      elif x > offset:
        new_grid[y][offset - x] = new_grid[y][offset - x] or value
  return new_grid, new_dimensions


def fold_y(grid, dimensions, offset):
  new_dimensions = {
    'width': dimensions['width'],
    'height': max(offset, dimensions['height'] - offset - 1),
  }
  new_grid = empty_grid(new_dimensions)
  for y, line in enumerate(grid):
    for x, value in enumerate(line):
      if y < offset:
        new_grid[y][x] = value
      elif y > offset:
        new_grid[offset - y][x] = new_grid[offset - y][x] or value
  return new_grid, new_dimensions


def run():
  points = []
  folds = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      if ',' in line:
        points.append([int(num) for num in line.strip().split(',')])
      elif 'x' in line:
        folds.append(['x', int(line.strip().split('=')[-1])])
      elif 'y' in line:
        folds.append(['y', int(line.strip().split('=')[-1])])

  dimensions = {
    'width': max(point[0] for point in points) + 1,
    'height': max(point[1] for point in points) + 1,
  }

  grid = empty_grid(dimensions)
  for point in points:
    grid[point[1]][point[0]] = True
  if folds[0][0] == 'x':
    grid, dimensions = fold_x(grid, dimensions, folds[0][1])
  else:
    grid, dimensions = fold_y(grid, dimensions, folds[0][1])
  print(sum(line.count(True) for line in grid))


if __name__ == '__main__':
  run()
