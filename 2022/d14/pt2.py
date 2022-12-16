SOURCE_FILE = 'numbers.txt'
START_X = 500


def print_cave(cave):
  for line in cave:
    print(line)


def is_out_of_bounds(cave: list[list[int]], point: [int, int]):
  return point[0] < 0 or point[1] < 0 or point[0] >= len(cave[0]) or point[1] >= len(cave)


def drop_sand(cave: list[list[int]], min_x: int):
  sand_dropped = 0
  start_position = [START_X - min_x, 0]
  while True:
    current_position = start_position
    while True:
      if cave[current_position[1] + 1][current_position[0]] == 0:
        current_position = [current_position[0], current_position[1] + 1]
      elif cave[current_position[1] + 1][current_position[0] - 1] == 0:
        current_position = [current_position[0] - 1, current_position[1] + 1]
      elif cave[current_position[1] + 1][current_position[0] + 1] == 0:
        current_position = [current_position[0] + 1, current_position[1] + 1]
      else:
        break
    if current_position[0] == start_position[0] and current_position[1] == start_position[1]:
      return sand_dropped + 1
    cave[current_position[1]][current_position[0]] = 1
    sand_dropped += 1


FLOOR_OFFSET = 2


def run():
  paths = []
  min_x = 9999999999
  max_x = -9999999999
  max_y = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      path_points = [[int(coord) for coord in point.strip().split(',')] for point in line.strip().split(' -> ')]
      for point in path_points:
        if point[1] > max_y:
          max_y = point[1]
        if point[0] > max_x:
          max_x = point[0]
        if point[0] < min_x:
          min_x = point[0]
      paths.append(path_points)

  max_y += FLOOR_OFFSET
  falling_sand_max_x = START_X + max_y
  falling_sand_min_x = START_X - max_y
  max_x = max(falling_sand_max_x, max_x)
  min_x = min(falling_sand_min_x, min_x)
  normalized_max_x = max_x - min_x

  cave = [[0] * (normalized_max_x + 1) for _ in range(max_y)]
  cave.append([1] * (normalized_max_x + 1))

  # set rocks
  for path in paths:
    for idx in range(len(path) - 1):
      start = path[idx]
      end = path[idx + 1]

      offset = [b_i - a_i for a_i, b_i in zip(start, end)]
      normalized_offset = [int(value / abs(value)) if value != 0 else 0 for value in offset]
      for jdx in range(max([abs(value) for value in offset]) + 1):
        cave[start[1] + normalized_offset[1] * jdx][start[0] - min_x + normalized_offset[0] * jdx] = 1

  print(drop_sand(cave, min_x))


if __name__ == '__main__':
  run()
