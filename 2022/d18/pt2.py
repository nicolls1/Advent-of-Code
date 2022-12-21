from sortedcontainers import SortedList

SOURCE_FILE = 'numbers.txt'

OFFSETS = {
  'up': [0, 1, 0],
  'down': [0, -1, 0],
  'left': [-1, 0, 0],
  'right': [1, 0, 0],
  'front': [0, 0, 1],
  'back': [0, 0, -1],
}


def add_positions(p1, p2):
  return [a + b for a, b in zip(p1, p2)]


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


def manhattan_distance(p1, p2):
  return sum([abs(value - p2[idx]) for idx, value in enumerate(p1)])


EXIT_POINT = [0, 0, 0]
reach_exit_cache = {}


def cache_positions(positions: list[list[int]], value: bool):
  for position in positions:
    reach_exit_cache[position_to_string(position)] = value


def can_reach_exit(point: list[int], all_points: list[list[int]]):
  all_visited = []
  queue = SortedList(key=lambda value: manhattan_distance(value, EXIT_POINT))
  queue.add(point)

  while len(queue) > 0:
    current = queue.pop(index=0)
    all_visited.append(current)
    position_string = position_to_string(current)
    if position_string in reach_exit_cache:
      cache_value = reach_exit_cache[position_string]
      cache_positions(all_visited, cache_value)
      return cache_value

    if current == EXIT_POINT:
      # add all points to queue
      cache_positions(all_visited, True)
      return True

    # add neighbors
    for offset in OFFSETS.values():
      new_position = add_positions(offset, current)
      if new_position not in all_points and new_position not in all_visited and new_position not in queue:
        queue.add(new_position)

  cache_positions(all_visited, False)
  return False


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

  count = 0
  all_points_list = [point.position for point in points.values()]
  for point in points.values():
    for direction, offset in OFFSETS.items():
      if getattr(point, direction) is None:
        neighbor_position = add_positions(point.position, offset)
        if can_reach_exit(neighbor_position, all_points_list):
          count += 1
  print(count)


if __name__ == '__main__':
  run()
