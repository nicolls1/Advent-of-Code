from collections import defaultdict

SOURCE_FILE = 'numbers.txt'

CHAR_POINTS = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
}

CHARACTER_PAIRINGS = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>',
}


def run():
  data = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      data.append(line.strip())

  illegal_character_counts = defaultdict(int)
  for line in data:
    stack = []
    for char in line:
      if char in CHARACTER_PAIRINGS.keys():
        stack.append(char)
      else:
        if CHARACTER_PAIRINGS[stack.pop()] != char:
          illegal_character_counts[char] += 1
          break

  print(sum([CHAR_POINTS[char] * count for char, count in illegal_character_counts.items()]))


if __name__ == '__main__':
  run()
