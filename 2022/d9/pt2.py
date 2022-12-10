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
  if horizontal_offset == 0:
    return [tail_position[0], tail_position[1] + int(vertical_offset / abs(vertical_offset))]
  # horizontal move needed
  if vertical_offset == 0:
    return [tail_position[0] + int(horizontal_offset / abs(horizontal_offset)), tail_position[1]]
  # diagonal move needed
  if abs(vertical_offset) >= 2:
    return [tail_position[0] + int(horizontal_offset / abs(horizontal_offset)),
            tail_position[1] + int(vertical_offset / abs(vertical_offset))]
  return [tail_position[0] + int(horizontal_offset / abs(horizontal_offset)),
          tail_position[1] + int(vertical_offset / abs(vertical_offset))]


DIRECTION_OFFSETS = {
  'U': [0, 1],
  'R': [1, 0],
  'D': [0, -1],
  'L': [-1, 0],
}


def run():
  head_position = [0, 0]
  tails_positions = [[0, 0]] * 9
  visited_positions = set()
  visited_positions.add(position_to_string(tails_positions[-1]))
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      direction, count = line.strip().split(' ')
      for _ in range(int(count)):
        head_position = [sum(i) for i in zip(head_position, DIRECTION_OFFSETS[direction])]
        tail_parent = head_position
        for i in range(len(tails_positions)):
          tails_positions[i] = get_next_tail_position(tail_parent, tails_positions[i])
          tail_parent = tails_positions[i]
        visited_positions.add(position_to_string(tails_positions[-1]))

  print(len(visited_positions))


if __name__ == '__main__':
  run()
