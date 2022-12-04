SOURCE_FILE = 'numbers.txt'


def run():
  duplicates = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      left, right = [line[:int(len(line) / 2)], line[int(len(line) / 2):]]

      duplicates.append(set(left).intersection(set(right)).pop())
  print(sum([ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27 for item in duplicates]))


if __name__ == '__main__':
  run()
