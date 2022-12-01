SOURCE_FILE = 'numbers.txt'
ROCKET_START = [0, 0]


def get_next_x_velocity(x_velocity):
  if x_velocity == 0:
    return 0
  if x_velocity > 0:
    return x_velocity - 1
  return x_velocity + 1


def get_rocket_path(target, start_position, start_velocity):
  positions = []
  current_position = [*start_position]
  current_velocity = [*start_velocity]
  while current_position[0] <= target[0][1] and current_position[1] >= target[1][0]:
    current_position = [current_position[0] + current_velocity[0], current_position[1] + current_velocity[1]]
    positions.append(current_position)
    current_velocity = [get_next_x_velocity(current_velocity[0]), current_velocity[1] - 1]
  return positions


def path_hits_target(target, path):
  for point in path:
    if target[0][0] <= point[0] <= target[0][1] and target[1][0] <= point[1] <= target[1][1]:
      return True
  return False


def max_y(path):
  return max(point[1] for point in path)


def run():
  with open(SOURCE_FILE, 'r') as f:
    line = f.readline().strip()
  x_range = [int(value) for value in line.split('=')[1][:-3].split('..')]
  y_range = [int(value) for value in line.split('=')[2].split('..')]
  target = (x_range, y_range)

  max_y_list = []
  for x_velocity in range(0, target[0][1] * 2):
    for y_velocity in range(0, abs(target[1][0]) * 5):
      path = get_rocket_path(target, ROCKET_START, [x_velocity, y_velocity])
      if path_hits_target(target, path):
        max_y_list.append(max_y(path))
  print(max(max_y_list))


if __name__ == '__main__':
  run()
