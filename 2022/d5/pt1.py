import re

SOURCE_FILE = 'numbers.txt'


def run():
  start_containers = []
  commands = []
  found_board_end = False
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      if found_board_end:
        if len(line.strip()) > 0:
          commands.append(line.strip())
      else:
        start_containers.append(line[:-1])

      if not found_board_end and line[1] == '1':
        found_board_end = True

  containers = int(start_containers[-1].strip()[-1])
  start_containers = start_containers[:-1]
  start_containers = start_containers[::-1]

  container_stacks = [[] for _ in range(containers)]
  for container in start_containers:
    for match in re.finditer(r'\[([A-Z])\]', container):
      container_stacks[int(match.start() / 4)].append(match.group()[1])

  for command in commands:
    match = re.match(r'move (.*) from (.*) to (.*)', command)
    move_count = int(match.groups()[0])
    move_start = int(match.groups()[1]) - 1
    move_end = int(match.groups()[2]) - 1

    for i in range(move_count):
      container_stacks[move_end].append(container_stacks[move_start].pop())

  print('stacks', ''.join([stack[-1] for stack in container_stacks]))


if __name__ == '__main__':
  run()
