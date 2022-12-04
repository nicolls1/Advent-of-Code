SOURCE_FILE = 'numbers.txt'


def run():
  duplicates = []
  with open(SOURCE_FILE, 'r') as f:
    lines = f.readlines()

  for i in range(int(len(lines) / 3)):
    first = lines[i * 3].strip()
    second = lines[i * 3 + 1].strip()
    third = lines[i * 3 + 2].strip()

    duplicates.append(set(first).intersection(set(second)).intersection(set(third)).pop())
  print(duplicates)
  print([ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27 for item in duplicates])
  print(sum([ord(item) - ord('a') + 1 if item.islower() else ord(item) - ord('A') + 27 for item in duplicates]))


if __name__ == '__main__':
  run()
