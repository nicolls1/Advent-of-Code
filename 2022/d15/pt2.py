import re
from typing import Union

import intervaltree

SOURCE_FILE = 'numbers.txt'
INSPECT_ROW = 2000000
MAX_HEIGHT = 4000000
MAX_WIDTH = 4000000


def manhattan_distance(p1, p2):
  return sum([abs(value - p2[idx]) for idx, value in enumerate(p1)])


def join_ranges(ranges: list[list[int]], points: list[int]):
  tree = intervaltree.IntervalTree.from_tuples(ranges)
  tree.merge_overlaps(strict=False)
  tree_items = list(tree)
  for idx in range(len(tree_items) - 1):
    current = tree_items[idx]
    next = tree_items[idx + 1]
    if current[1] + 1 == next[0]:
      tree.add(intervaltree.Interval(current[1], next[0]))

  ignore_points = []
  for point in points:
    if not tree.overlaps(point):
      ignore_points.append(point)

  return list(tree), ignore_points


def find_empty_positions_for_row(row: int, locations: list[dict[str, Union[int, list[int]]]]):
  empty_ranges = []
  points = []
  for location in locations:
    y_distance = abs(location['sensor'][1] - row)
    if y_distance < location['distance']:
      distance_difference = location['distance'] - y_distance
      empty_ranges.append([max(location['sensor'][0] - distance_difference, 0),
                           min(location['sensor'][0] + distance_difference, MAX_WIDTH)])
    elif y_distance == location['distance']:
      points.append(y_distance)

  return join_ranges(empty_ranges, points)


def run():
  locations = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      match = re.match(r'Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)', line.strip())
      sensor = [int(match.groups()[0]), int(match.groups()[1])]
      beacon = [int(match.groups()[2]), int(match.groups()[3])]
      locations.append({
        'sensor': sensor,
        'beacon': beacon,
        'distance': manhattan_distance(sensor, beacon)
      })

  y_position = -1
  for idx in range(MAX_HEIGHT):
    if idx % 1000 == 0:
      print(idx)
    empty_positions, points = find_empty_positions_for_row(idx, locations)
    if len(empty_positions) - len(points) > 1:
      y_position = idx
      break

  print((empty_positions[0][1] + 1) * 4000000 + y_position)


if __name__ == '__main__':
  run()
