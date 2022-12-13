import json
import math
from functools import cmp_to_key

SOURCE_FILE = 'numbers.txt'


def make_list_if_not(value):
  return value if isinstance(value, list) else [value]


def compare_list(left, right):
  for i in range(len(left)):
    left_value = left[i]
    if len(right) - 1 < i:
      return 1
    right_value = right[i]
    if isinstance(left_value, list) or isinstance(right_value, list):
      result = compare_list(make_list_if_not(left_value), make_list_if_not(right_value))
      if result is not None:
        return result
    elif left_value < right_value:
      return -1
    elif left_value > right_value:
      return 1

  if len(left) < len(right):
    return -1
  elif len(left) > len(right):
    return 1
  return None


DIVIDERS = [[[2]], [[6]]]


def run():
  # decoder packets
  packets = [*DIVIDERS]
  with open(SOURCE_FILE, 'r') as f:
    while True:
      packets.append(json.loads(f.readline().strip()))
      packets.append(json.loads(f.readline().strip()))

      if len(f.readline()) == 0:
        break

  packets.sort(key=cmp_to_key(compare_list))
  dividers_indices = []
  for idx, packet in enumerate(packets):
    if packet in DIVIDERS:
      dividers_indices.append(idx + 1)

  print(math.prod(dividers_indices))


if __name__ == '__main__':
  run()
