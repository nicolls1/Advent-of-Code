SOURCE_FILE = 'numbers.txt'
HUMAN_KEY = 'humn'

OPERATIONS = {
  '+': lambda left, right: left + right,
  '-': lambda left, right: left - right,
  '/': lambda left, right: left / right,
  '*': lambda left, right: left * right,
}

INVERSE_OPERATIONS = {
  '+': lambda total, left=None, right=None: total - right if left is None else total - left,
  '-': lambda total, left=None, right=None: total + right if left is None else left - total,
  '/': lambda total, left=None, right=None: total * right if left is None else left / total,
  '*': lambda total, left=None, right=None: total / right if left is None else total / left,
}


class Node:
  def __init__(self, value=None, left=None, right=None, operation=None):
    self.value = value
    self.left = left
    self.right = right
    self.operation = operation

  def __str__(self):
    return str(self.value) if self.value else f'{self.left} {self.operation} {self.right}'


def get_node_value(node: Node, all_nodes: dict[str, Node]):
  if node.value:
    return node.value
  if node.value is None and node.left is None and node.right is None:
    return None

  left = get_node_value(all_nodes[node.left], all_nodes)
  right = get_node_value(all_nodes[node.right], all_nodes)
  if left is None or right is None:
    return None
  node.value = OPERATIONS[node.operation](left, right)
  return node.value


def solve_node(node: Node, end_value: int, all_nodes: dict[str, Node]):
  next_node = None
  if node.right is not None and all_nodes[node.right].value:
    result = INVERSE_OPERATIONS[node.operation](end_value, None, all_nodes[node.right].value)
    node.value = result
    next_node = all_nodes[node.left]
  if node.left is not None and all_nodes[node.left].value:
    result = INVERSE_OPERATIONS[node.operation](end_value, all_nodes[node.left].value, None)
    node.value = result
    next_node = all_nodes[node.right]
  if next_node is not None:
    solve_node(next_node, result, all_nodes)
  else:
    node.value = end_value


def run():
  nodes = {}
  root: Node
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      name, value = line.strip().split(':')
      if name == HUMAN_KEY:
        nodes[name] = Node(value=None)
      elif value.strip().isdigit():
        nodes[name] = Node(value=int(value.strip()))
      else:
        parts = value.strip().split(' ')
        nodes[name] = Node(left=parts[0], right=parts[2], operation=parts[1])
        if name == 'root':
          root = nodes[name]

  left, right = get_node_value(nodes[root.left], nodes), get_node_value(nodes[root.right], nodes)

  if left is None:
    solve_node(nodes[root.left], right, nodes)
  else:
    solve_node(nodes[root.right], left, nodes)

  print(int(nodes[HUMAN_KEY].value))


if __name__ == '__main__':
  run()
