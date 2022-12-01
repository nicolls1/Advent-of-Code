import numpy as np

SOURCE_FILE = 'numbers.txt'
CHAR_MAP = {
  '.': 0,
  '>': 1,
  'v': 2
}


def run_iteration(grid, dimensions):
  next_grid = np.zeros((dimensions['height'], dimensions['width']), np.int8)
  moved = False
  # move right
  for y, line in enumerate(grid):
    for x, value in enumerate(line):
      if value == 1 and grid[y][(x + 1) % dimensions['width']] == 0:
        moved = True
        next_grid[y][(x + 1) % dimensions['width']] = value
      elif value == 1:
        next_grid[y][x] = value

  # move down
  for y, line in enumerate(grid):
    for x, value in enumerate(line):
      next_y = (y + 1) % dimensions['height']
      if value == 2 and (grid[next_y][x] == 0 or grid[next_y][x] == 1) and next_grid[next_y][x] == 0:
        moved = True
        next_grid[next_y][x] = value
      elif value == 2:
        next_grid[y][x] = value
  return next_grid, moved


def run():
  grid = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      grid.append([CHAR_MAP[char] for char in line.strip()])
  grid = np.array(grid)
  dimensions = {
    'height': len(grid),
    'width': len(grid[0])
  }
  current_grid = grid
  count = 0
  moved = True
  while moved:
    count += 1
    current_grid, moved = run_iteration(current_grid, dimensions)
  print(count)


if __name__ == '__main__':
  run()
