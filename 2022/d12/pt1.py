import sys

SOURCE_FILE = 'numbers.txt'

DIRECTION_OFFSET = {
  'up': {
    'x': 0,
    'y': -1,
  },
  'right': {
    'x': 1,
    'y': 0,
  },
  'down': {
    'x': 0,
    'y': 1,
  },
  'left': {
    'x': -1,
    'y': 0,
  },
}


def is_out_of_bounds(x: int, y: int, width: int, height: int):
  return x < 0 or y < 0 or x >= width or y >= height


class Node:
  def __init__(self, height: str):
    self.height = height
    self.up = None
    self.right = None
    self.down = None
    self.left = None
    self.distance = sys.maxsize
    self.end = False

  def __str__(self):
    return f'{self.height}: {"." if self.up is None else "^"} {"." if self.right is None else ">"} ' + \
           f'{"." if self.down is None else "v"} {"." if self.left is None else "<"} e:{self.end}'


def print_heights(grid: list[list[Node]]):
  for line in grid:
    print(' '.join([' ' + node.height for node in line]))


def print_distances(grid: list[list[Node]]):
  for line in grid:
    print(' '.join([str(node.distance).zfill(2) for node in line]))


def build_graph(grid: list[list[Node]]):
  grid_width = len(grid[0])
  grid_height = len(grid)

  for y in range(grid_height):
    for x in range(grid_width):
      for key, value in DIRECTION_OFFSET.items():
        inspect_x = x + value['x']
        inspect_y = y + value['y']
        max_traversable = chr(ord(grid[y][x].height) + 1)
        if not is_out_of_bounds(inspect_x, inspect_y, grid_width, grid_height) and \
            grid[inspect_y][inspect_x].height <= max_traversable:
          grid[y][x].__setattr__(key, grid[inspect_y][inspect_x])


def fill_distances(start):
  start.distance = 0
  nodes_queue = [start]

  while len(nodes_queue) > 0:
    current = nodes_queue.pop(0)
    neighbors = [current.up, current.right, current.down, current.left]
    new_distance = current.distance + 1
    for neighbor in neighbors:
      if neighbor is not None and new_distance < neighbor.distance:
        neighbor.distance = new_distance
        nodes_queue.append(neighbor)
        if neighbor.end:
          return


def run():
  grid = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      grid.append([Node(char) for char in list(line.strip())])

  # mark start and end
  start = None
  end = None
  for row in grid:
    for node in row:
      if node.height == 'S':
        start = node
        start.height = 'a'
      elif node.height == 'E':
        end = node
        end.end = True
        end.height = 'z'

  build_graph(grid)
  fill_distances(start)

  # print_heights(grid)
  # print_distances(grid)
  print(end.distance)


if __name__ == '__main__':
  run()
