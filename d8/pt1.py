SOURCE_FILE = './numbers.txt'


def run():
  combinations = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      parts = line.strip().split('|')
      combinations.append({
        'inputs': parts[0].strip().split(' '),
        'outputs': parts[1].strip().split(' '),
      })

  count = 0
  for combination in combinations:
    for output in combination['outputs']:
      if len(output) in [2, 3, 4, 7]:
        count += 1
  print(count)


if __name__ == '__main__':
  run()
