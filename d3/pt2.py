SOURCE_FILE = './numbers.txt'


def find_common_number_at_idx(numbers, idx, most_common):
  counts = [0, 0]
  for number in numbers:
    counts[int(number[idx])] += 1
  if counts[0] == counts[1]:
    return 1 if most_common else 0
  elif counts[0] > counts[1]:
    return 0 if most_common else 1
  elif counts[0] < counts[1]:
    return 1 if most_common else 0


def filter_numbers_by_idx_pos(numbers, most_common):
  idx = 0
  while len(numbers) > 1:
    keep_number = find_common_number_at_idx(numbers, idx, most_common)
    numbers = list(filter(lambda number: int(number[idx]) == keep_number, numbers))
    idx += 1
  return int(numbers[0], 2)


def run():
  numbers = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      numbers.append(line.strip())

  oxygen = filter_numbers_by_idx_pos(numbers.copy(), True)
  co2 = filter_numbers_by_idx_pos(numbers.copy(), False)

  print(oxygen * co2)


if __name__ == '__main__':
  run()
