SOURCE_FILE = 'numbers.txt'

OPERATIONS = {
  '+': lambda left, right: left + right,
  '-': lambda left, right: left - right,
  '/': lambda left, right: left / right,
  '*': lambda left, right: left * right,
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

  left = get_node_value(all_nodes[node.left], all_nodes)
  right = get_node_value(all_nodes[node.right], all_nodes)
  return OPERATIONS[node.operation](left, right)


def run():
  nodes = {}
  root: Node
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      name, value = line.strip().split(':')
      if value.strip().isdigit():
        nodes[name] = Node(value=int(value.strip()))
      else:
        parts = value.strip().split(' ')
        nodes[name] = Node(left=parts[0], right=parts[2], operation=parts[1])
        if name == 'root':
          root = nodes[name]
  print(int(get_node_value(root, nodes)))


if __name__ == '__main__':
  run()
