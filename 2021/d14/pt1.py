from collections import Counter

SOURCE_FILE = 'numbers.txt'
ITERATIONS = 10


def run_iteration(template, mapping):
  new_template = ''
  for index, value in enumerate(template):
    new_template += value
    if index == len(template) - 1:
      continue
    new_template += mapping[value + template[index + 1]]
  return new_template


def run():
  mapping = {}
  with open(SOURCE_FILE, 'r') as f:
    template = f.readline().strip()
    f.readline()
    for line in f:
      key, value = line.split('->')
      mapping[key.strip()] = value.strip()

  for _ in range(ITERATIONS):
    template = run_iteration(template, mapping)

  char_count = Counter(template)
  print(char_count)
  print(max(char_count.values()) - min(char_count.values()))


if __name__ == '__main__':
  run()
