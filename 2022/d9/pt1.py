SOURCE_FILE = 'numbers.txt'


def position_to_string(position: [int, int]):
  return ','.join([str(dim) for dim in position])


def get_next_tail_position(head_position: [int, int], tail_position: [int, int]):
  vertical_offset = head_position[1] - tail_position[1]
  horizontal_offset = head_position[0] - tail_position[0]

  # no change needed
  if abs(vertical_offset) + abs(horizontal_offset) <= 1 or (abs(vertical_offset) == 1 and abs(horizontal_offset) == 1):
    return tail_position
  # vertical move needed
  if abs(vertical_offset) == 2 and horizontal_offset == 0:
    return [tail_position[0], tail_position[1] + int(vertical_offset / 2)]
  # horizontal move needed
  if vertical_offset == 0 and abs(horizontal_offset) == 2:
    return [tail_position[0] + int(horizontal_offset / 2), tail_position[1]]
  # diagonal move needed
  if abs(vertical_offset) == 2:
    return [tail_position[0] + horizontal_offset, tail_position[1] + int(vertical_offset / 2)]
  return [tail_position[0] + int(horizontal_offset / 2), tail_position[1] + vertical_offset]


DIRECTION_OFFSETS = {
  'U': [0, 1],
  'R': [1, 0],
  'D': [0, -1],
  'L': [-1, 0],
}


def run():
  head_position = [0, 0]
  tail_position = [0, 0]
  visited_positions = set()
  visited_positions.add(position_to_string(tail_position))
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      direction, count = line.strip().split(' ')
      for _ in range(int(count)):
        head_position = [sum(i) for i in zip(head_position, DIRECTION_OFFSETS[direction])]
        tail_position = get_next_tail_position(head_position, tail_position)
        visited_positions.add(position_to_string(tail_position))

  print(len(visited_positions))


if __name__ == '__main__':
  run()
