import heapq

SOURCE_FILE = 'numbers.txt'


def get_position_key(x, y):
  return f'{x},{y}'


def get_position_value(data, x, y):
  return data[y][x]


def is_inside(dimensions, x, y):
  return dimensions['width'] > x >= 0 and dimensions['height'] > y >= 0


def get_neighbors(dimensions, x, y):
  neighbors = []
  if is_inside(dimensions, x - 1, y):
    neighbors.append([x - 1, y])
  if is_inside(dimensions, x + 1, y):
    neighbors.append([x + 1, y])
  if is_inside(dimensions, x, y - 1):
    neighbors.append([x, y - 1])
  if is_inside(dimensions, x, y + 1):
    neighbors.append([x, y + 1])
  return neighbors


def run():
  data = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      data.append([int(value) for value in line.strip()])

  dimensions = {
    'width': len(data[0]),
    'height': len(data),
  }

  start_position = [0, 0]
  end_position = [dimensions['width'] - 1, dimensions['height'] - 1]
  parents = {
    get_position_key(*start_position): None
  }
  position_costs = {}
  available_nodes = [
    (0, start_position)
  ]
  while len(available_nodes) > 0:
    current_node = heapq.heappop(available_nodes)
    position_costs[get_position_key(*current_node[1])] = current_node[0]
    neighbors = get_neighbors(dimensions, *current_node[1])
    for neighbor in neighbors:
      # skip nodes already visited, we can do this because of consistent cost to visit node from other nodes
      if get_position_key(*neighbor) in parents:
        continue
      parents[get_position_key(*neighbor)] = current_node[1]
      heapq.heappush(available_nodes, (current_node[0] + get_position_value(data, *neighbor), neighbor))
    if get_position_key(*end_position) in parents:
      break

  total_risk = 0
  current_position = end_position
  while current_position:
    total_risk += get_position_value(data, *current_position)
    current_position = parents[get_position_key(*current_position)]

  print(total_risk - get_position_value(data, *start_position))


if __name__ == '__main__':
  run()
