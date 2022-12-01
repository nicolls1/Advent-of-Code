from functools import reduce

SOURCE_FILE = 'numbers.txt'

CHAR_POINTS = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4,
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

  incomplete_stacks = []
  for line in data:
    stack = []
    error = False
    for char in line:
      if char in CHARACTER_PAIRINGS.keys():
        stack.append(char)
      else:
        if CHARACTER_PAIRINGS[stack.pop()] != char:
          error = True
          break
    if not error:
      incomplete_stacks.append(stack)

  line_scores = []
  for line in incomplete_stacks:
    remaining_chars = [CHARACTER_PAIRINGS[line.pop()] for _ in range(len(line))]
    line_scores.append(reduce(lambda score_sum, char: (score_sum * 5) + CHAR_POINTS[char], remaining_chars, 0))

  line_scores.sort()
  print(line_scores[int((len(line_scores) - 1) / 2)])


if __name__ == '__main__':
  run()
