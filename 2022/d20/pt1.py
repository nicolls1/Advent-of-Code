SOURCE_FILE = 'numbers.txt'
interesting_positions = [1000, 2000, 3000]


class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None

  def __str__(self):
    return f'{self.value}'


def get_shortest_move(length: int, shift: int):
  return abs(shift) % (length - 1)


def get_left(node: Node, amount: int):
  current = node
  move_count = abs(amount) + 1
  for i in range(move_count):
    current = current.left
  return current


def get_right(node: Node, amount: int):
  current = node
  move_count = abs(amount)
  for i in range(move_count):
    current = current.right
  return current


def get_values(start: Node, count: int):
  values = []
  current = start
  for _ in range(count):
    values.append(current.value)
    current = current.right
  return values


def run():
  nodes = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      nodes.append(Node(int(line.strip())))

  nodes_count = len(nodes)

  # connect
  start: Node
  for idx, node in enumerate(nodes):
    node.left = nodes[(idx - 1) % nodes_count]
    node.right = nodes[(idx + 1) % nodes_count]
    if node.value == 0:
      start = node

  for node in nodes:
    shortest_move = get_shortest_move(nodes_count, node.value)
    # shortest_move = node.value
    if shortest_move == 0:
      continue
    elif node.value < 0:
      new_position_left = get_left(node, shortest_move)
    else:
      new_position_left = get_right(node, shortest_move)

    # remove from old
    node.left.right = node.right
    node.right.left = node.left

    # add new
    node.left = new_position_left
    node.right = new_position_left.right
    node.right.left = node
    node.left.right = node

  end_values = get_values(start, len(nodes))

  interesting_offsets = [pos % nodes_count for pos in interesting_positions]
  print(sum(end_values[offset] for offset in interesting_offsets))


if __name__ == '__main__':
  run()
