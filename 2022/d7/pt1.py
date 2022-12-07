from typing import TextIO, List

SOURCE_FILE = 'numbers.txt'


class Folder(object):
  def __init__(self, parent, name):
    self.parent = parent
    self.name = name
    self.children = {}
    self.size = 0


class File:
  def __init__(self, size, name):
    self.size = size
    self.name = name


def cd(command: List[str], current: Folder, _f: TextIO):
  new_folder = command[2]

  if new_folder == '..':
    return current.parent

  assert new_folder in current.children
  return current.children[new_folder]


def ls(_command: List[str], current: Folder, f: TextIO):
  while True:
    pos = f.tell()
    line = f.readline().strip()

    if len(line) == 0 or line[0] == '$':
      f.seek(pos)
      return current

    line_parts = line.split(' ')
    if line_parts[0] == 'dir':
      # folder
      current.children[line_parts[1]] = Folder(current, line_parts[1])
    else:
      # file
      current.children[line_parts[1]] = File(int(line_parts[0]), line_parts[1])


COMMANDS = {
  'cd': cd,
  'ls': ls,
}


def read_file(f: TextIO):
  root_command = f.readline()
  assert root_command, '$ cd /'
  root = Folder(None, '/')
  current = root

  while True:
    line = f.readline().strip()
    if len(line) == 0:
      return root
    command_parts = line.split(' ')
    current = COMMANDS[command_parts[1]](command_parts, current, f)


def sum_sizes(root: Folder):
  for child in root.children.values():
    if isinstance(child, Folder):
      sum_sizes(child)

  root.size = sum([value.size for value in root.children.values()])


def sum_sizes_below_value(root: Folder, value: int):
  local_sum = 0
  if root.size < value:
    local_sum += root.size

  for child in root.children.values():
    if isinstance(child, Folder):
      local_sum += sum_sizes_below_value(child, value)

  return local_sum


MAX_FOLDER_SIZE = 100000


def run():
  with open(SOURCE_FILE, 'r') as f:
    root = read_file(f)
  sum_sizes(root)

  print(sum_sizes_below_value(root, MAX_FOLDER_SIZE))


if __name__ == '__main__':
  run()
