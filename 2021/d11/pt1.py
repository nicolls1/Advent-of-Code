SOURCE_FILE = 'numbers.txt'

# defined in problem
dimensions = {
  'width': 10,
  'height': 10,
}
ITERATION_COUNT = 100


def print_data(data):
  print(
    '\n'.join([''.join([str(p) for p in row]) for row in data])
  )
  print()


def is_inside(x, y):
  return dimensions['width'] > x >= 0 and dimensions['height'] > y >= 0


def increment_neighbors(data, x, y):
  # self increment doesn't really matter
  for x_offset in range(-1, 2):
    for y_offset in range(-1, 2):
      if is_inside(x + x_offset, y + y_offset):
        data[y + y_offset][x + x_offset] += 1


def run_iteration(data):
  # increment all cells
  for y in range(dimensions['height']):
    for x in range(dimensions['width']):
      data[y][x] += 1

  # check if any went over 9
  visited = [[False for _ in range(dimensions['width'])] for _ in range(dimensions['height'])]
  while True:
    incremented = False
    for y in range(dimensions['height']):
      for x in range(dimensions['width']):
        if not visited[y][x] and data[y][x] > 9:
          incremented = True
          visited[y][x] = True
          increment_neighbors(data, x, y)
    if not incremented:
      break

  # reset visited cells
  visited_count = 0
  for y, rows in enumerate(visited):
    for x, visited in enumerate(rows):
      if visited:
        visited_count += 1
        data[y][x] = 0
  return visited_count


def run():
  data = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      data.append([int(c) for c in line.strip()])

  lights_sum = 0
  for _ in range(ITERATION_COUNT):
    lights_sum += run_iteration(data)
  print(lights_sum)


if __name__ == '__main__':
  run()
