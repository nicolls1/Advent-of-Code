from collections import Counter

SOURCE_FILE = 'numbers.txt'
ITERATIONS = 40


def get_key(value, level):
  return f'{value}-{level}'


def find_node_counts(mapping, cache, value, level):
  if get_key(value, level) in cache:
    return cache[get_key(value, level)]
  if level == ITERATIONS:
    return Counter(value)

  new_char = mapping[value]
  left_sum = find_node_counts(mapping, cache, value[0] + new_char, level + 1)
  right_sum = find_node_counts(mapping, cache, new_char + value[1], level + 1)
  counts = left_sum + right_sum + Counter({new_char: - 1})
  cache[get_key(value, level)] = counts
  return counts


def run():
  cache = {}
  mapping = {}
  with open(SOURCE_FILE, 'r') as f:
    template = f.readline().strip()
    f.readline()
    for line in f:
      key, value = line.split('->')
      mapping[key.strip()] = value.strip()

  char_count = Counter()
  for index, value in enumerate(template):
    if index == len(template) - 1:
      continue
    char_count += find_node_counts(mapping, cache, value + template[index + 1], 0) - Counter(
      template[index + 1] if not index + 1 == len(template) - 1 else '')
  print(char_count)
  print(max(char_count.values()) - min(char_count.values()))


if __name__ == '__main__':
  run()
