SOURCE_FILE = 'numbers.txt'

INTERESTING_CYCLES = [20, 60, 100, 140, 180, 220]


def value_if_interesting_cycle(cycle: int, register_value: int):
  if cycle in INTERESTING_CYCLES:
    return register_value * cycle
  return 0


def run():
  cycle = 1
  register_value = 1
  interesting_total = 0
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      line_parts = line.strip().split()
      interesting_total += value_if_interesting_cycle(cycle, register_value)
      if line_parts[0] == 'noop':
        cycle += 1
      elif line_parts[0] == 'addx':
        cycle += 1
        interesting_total += value_if_interesting_cycle(cycle, register_value)
        cycle += 1
        register_value += int(line_parts[1])

  print(interesting_total)


if __name__ == '__main__':
  run()
