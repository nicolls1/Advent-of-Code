import re
from typing import Union

SOURCE_FILE = 'numbers.txt'
INSPECT_ROW = 2000000


def manhattan_distance(p1, p2):
  return sum([abs(value - p2[idx]) for idx, value in enumerate(p1)])


def point_to_string(point: list[int]):
  return ','.join([str(p) for p in point])


def find_empty_positions_for_row(row: int, locations: list[dict[str, Union[int, list[int]]]]):
  empty_locations = set()
  for location in locations:
    y_distance = abs(location['sensor'][1] - row)
    if y_distance <= location['distance']:
      distance_difference = location['distance'] - y_distance
      for idx in range(-distance_difference, distance_difference):
        empty_locations.add(point_to_string([location['sensor'][0] + idx, row]))

  return empty_locations


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

  print(len(find_empty_positions_for_row(INSPECT_ROW, locations)))


if __name__ == '__main__':
  run()
