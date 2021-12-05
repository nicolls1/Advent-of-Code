from collections import defaultdict

SOURCE_FILE = './numbers.txt'


def run():
  lines = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      points = line.split('->')
      lines.append([[int(coord) for coord in point.strip().split(',')] for point in points])

  position_counts = defaultdict(lambda: defaultdict(int))
  for line in lines:
    if line[0][0] == line[1][0]:
      # vertical
      start = line[1] if line[0][1] > line[1][1] else line[0]
      length = max(line[0][1], line[1][1]) - min(line[0][1], line[1][1]) + 1
      for idx in range(length):
        position_counts[start[0]][start[1] + idx] += 1
    elif line[0][1] == line[1][1]:
      # horizontal
      start = line[1] if line[0][0] > line[1][0] else line[0]
      length = max(line[0][0], line[1][0]) - min(line[0][0], line[1][0]) + 1
      for idx in range(length):
        position_counts[start[0] + idx][start[1]] += 1

  count = 0
  for idx, second in position_counts.items():
    for jdx, position_count in second.items():
      if position_count > 1:
        count += 1

  print(count)


if __name__ == '__main__':
  run()
