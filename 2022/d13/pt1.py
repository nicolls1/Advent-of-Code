import json

SOURCE_FILE = 'numbers.txt'


def make_list_if_not(value):
  return value if isinstance(value, list) else [value]


def compare_list(left, right):
  for i in range(len(left)):
    left_value = left[i]
    if len(right) - 1 < i:
      return False
    right_value = right[i]
    if isinstance(left_value, list) or isinstance(right_value, list):
      result = compare_list(make_list_if_not(left_value), make_list_if_not(right_value))
      if result is not None:
        return result
    elif left_value < right_value:
      return True
    elif left_value > right_value:
      return False

  if len(left) < len(right):
    return True
  elif len(left) > len(right):
    return False
  return None


def run():
  pairs = []
  with open(SOURCE_FILE, 'r') as f:
    while True:
      left = json.loads(f.readline().strip())
      right = json.loads(f.readline().strip())

      pairs.append([left, right])

      if len(f.readline()) == 0:
        break

  index_sum = 0
  for idx, pair in enumerate(pairs):
    index_sum += idx + 1 if compare_list(pair[0], pair[1]) else 0
  print(index_sum)


if __name__ == '__main__':
  run()
