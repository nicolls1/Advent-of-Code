from collections import defaultdict

import numpy as np

SOURCE_FILE = 'numbers.txt'
# X towards you, Z up/down, Y right/left
DIRECTION_ROTATIONS = [
  [  # none
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
  ],
  [  # left
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1],
  ],
  [  # right
    [0, 1, 0],
    [-1, 0, 0],
    [0, 0, 1],
  ],
  [  # up
    [0, 0, 1],
    [0, 1, 0],
    [-1, 0, 0],
  ],
  [  # down
    [0, 0, -1],
    [0, 1, 0],
    [1, 0, 0],
  ],
  [  # back
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, 1],
  ],
]

UP_ROTATIONS = [
  [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
  ],
  [
    [1, 0, 0],
    [0, 0, -1],
    [0, 1, 0],
  ],
  [
    [1, 0, 0],
    [0, 0, 1],
    [0, -1, 0],
  ],
  [
    [1, 0, 0],
    [0, -1, 0],
    [0, 0, -1],
  ],
]


def point_key(point):
  return ','.join([str(value) for value in point])


def normalize(points, center, rotation):
  inverse_center = np.dot(rotation, [-1 * value for value in center])
  rotated_points = [np.dot(rotation, point) for point in points]
  return [[sum(value) for value in zip(point, inverse_center)] for point in rotated_points]


def normalize_scanner(scanner, rotation):
  return [set([point_key(point) for point in normalize(scanner, point, rotation)]) for point in scanner]


def max_overlap(normalized_scanner_a, normalized_scanner_b):
  overlap_counts = []
  for index_a, points_a_set in enumerate(normalized_scanner_a):
    for index_b, points_b_set in enumerate(normalized_scanner_b):
      overlap_counts.append((len(points_a_set & points_b_set), (index_a, index_b)))
  return max(overlap_counts, key=lambda item: item[0])


def normalized_rotation_generator(normalized_rotated_scanners):
  for scanner_index, normalized_rotated_scanner in enumerate(normalized_rotated_scanners):
    for rotation_index, normalized_rotation in enumerate(normalized_rotated_scanner):
      yield scanner_index, rotation_index, normalized_rotation


def all_rotations():
  return [np.dot(direction_rotation, up_rotation) for direction_rotation in DIRECTION_ROTATIONS for up_rotation in
          UP_ROTATIONS]


def find_path(connections, start, visited):
  if start == 0:
    return [0]
  for connection in connections[start]:
    if connection not in visited:
      new_visited = {connection, *visited}
      path = find_path(connections, connection, new_visited)
      if path is not None:
        return [start, *path]


def scanner_offsets_key(a, b):
  return f'{a},{b}'


def run_transforms(points, transforms):
  current_points = [*points]
  for transform in transforms:
    # rotate
    current_points = [np.dot(transform[1], point) for point in current_points]
    # shift
    current_points = [[value + transform[0][idx] for idx, value in enumerate(point)] for point in current_points]
  return current_points


def run():
  scanners = []
  with open(SOURCE_FILE, 'r') as f:
    f.readline()
    scanner = []
    for line in f:
      if len(line.strip()) == 0:
        continue
      if '---' in line:
        scanners.append(scanner)
        scanner = []
        continue
      scanner.append([int(value) for value in line.strip().split(',')])
    scanners.append(scanner)

  # normalize the points in each scanner where each point is the center of the coordinate system
  normalized_rotated_scanners = [[normalize_scanner(scanner, rotation) for rotation in all_rotations()] for scanner in
                                 scanners]

  # find the offsets from any scanner to any other scanner using points that have overlap
  scanner_offsets = {}
  for scanner_index_b, normalized_rotated_scanner in enumerate(normalized_rotated_scanners):
    for scanner_index_a, rotation_index_a, normalized_rotation_a in \
        normalized_rotation_generator(normalized_rotated_scanners):
      if scanner_index_a == scanner_index_b:
        continue

      overlap, overlap_index = max_overlap(normalized_rotated_scanner[0], normalized_rotation_a)
      if overlap >= 12:
        point_a = scanners[scanner_index_b][overlap_index[0]]
        point_b = scanners[scanner_index_a][overlap_index[1]]
        rotated_b = np.dot(all_rotations()[rotation_index_a], point_b)
        scanner_offset = [values[0] - values[1] for values in zip(point_a, rotated_b)]
        scanner_offsets[scanner_offsets_key(scanner_index_b, scanner_index_a)] = (
          scanner_offset, all_rotations()[rotation_index_a])

  # Find path from scanner N to scanner 0
  connections = defaultdict(list)
  for path in scanner_offsets.keys():
    start, end = [int(value) for value in path.split(',')]
    connections[start].append(end)
    connections[end].append(start)

  paths = []
  for scanner_index in range(1, len(scanners)):
    paths.append(find_path(connections, scanner_index, set()))

  # Run the transformations on each of the paths
  path_transformations = [
    [scanner_offsets[scanner_offsets_key(path[idx + 1], point)] for idx, point in enumerate(path[:-1])] for path
    in paths]
  transformed_scanners = [
    scanners[0],
    *[run_transforms(points, path_transformations[idx]) for idx, points in enumerate(scanners[1:])]
  ]

  # find the unique points
  unique_points = {point_key(point) for scanner in transformed_scanners for point in scanner}
  print(len(unique_points))


if __name__ == '__main__':
  run()
