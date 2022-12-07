SOURCE_FILE = 'numbers.txt'
WINDOW_LENGTH = 4


def find_offset_window(data):
  for index in range(len(data) - 4):
    if len(set(data[index:index + WINDOW_LENGTH])) == WINDOW_LENGTH:
      return index + WINDOW_LENGTH

  return len(data)


def run():
  with open(SOURCE_FILE, 'r') as f:
    data = f.readline().strip()

  print(find_offset_window(data))


if __name__ == '__main__':
  run()
