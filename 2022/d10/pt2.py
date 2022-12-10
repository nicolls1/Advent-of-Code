import math

SOURCE_FILE = 'numbers.txt'


def set_screen_value_for_cycle(screen: list[list[str]], cycle: int, register_value: int):
  x = cycle % 40
  y = math.floor(cycle / 40)
  screen[y][x] = '#' if register_value - 1 <= x <= register_value + 1 else '.'


def run():
  cycle = 0
  register_value = 1
  screen = [list(' ' * 40) for _ in range(6)]
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      line_parts = line.strip().split()
      set_screen_value_for_cycle(screen, cycle, register_value)
      if line_parts[0] == 'noop':
        cycle += 1
      elif line_parts[0] == 'addx':
        cycle += 1
        set_screen_value_for_cycle(screen, cycle, register_value)
        cycle += 1
        register_value += int(line_parts[1])

  for row in screen:
    print(''.join(row))


if __name__ == '__main__':
  run()
