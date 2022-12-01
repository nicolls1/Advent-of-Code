import json
import math

SOURCE_FILE = 'numbers.txt'


class Node:
  def __init__(self, parent=None, value=None):
    self.parent = parent
    self.left = None
    self.right = None
    self.value = value

  def __str__(self):
    if self.value is not None:
      return str(self.value)
    return f'[{str(self.left)}, {str(self.right)}]'

  def get_rightmost_leaf(self):
    if self.right is None:
      return self
    return self.right.get_rightmost_leaf()

  def get_leftmost_leaf(self):
    if self.left is None:
      return self
    return self.left.get_leftmost_leaf()

  def get_right_leaf_neighbor(self):
    if self.parent is None:
      return None
    if self.parent.right is self:
      return self.parent.get_right_leaf_neighbor()
    return self.parent.right.get_leftmost_leaf()

  def get_left_leaf_neighbor(self):
    if self.parent is None:
      return None
    if self.parent.left is self:
      return self.parent.get_left_leaf_neighbor()
    return self.parent.left.get_rightmost_leaf()

  def explode(self):
    left_leaf_neighbor = self.get_left_leaf_neighbor()
    right_leaf_neighbor = self.get_right_leaf_neighbor()

    if left_leaf_neighbor is not None:
      left_leaf_neighbor.value += self.left.value
    if right_leaf_neighbor is not None:
      right_leaf_neighbor.value += self.right.value
    self.value = 0
    self.left = None
    self.right = None

  def split(self):
    self.left = Node(parent=self, value=math.floor(self.value / 2))
    self.right = Node(parent=self, value=math.ceil(self.value / 2))
    self.value = None

  def reduce_explode(self, depth):
    if depth == 4:
      if self.value is None:
        self.explode()
        return True

    if self.value is not None:
      return False

    left_exploded = self.left.reduce_explode(depth + 1)
    if left_exploded:
      return True
    return self.right.reduce_explode(depth + 1)

  def reduce_split(self, depth):
    if self.value is not None and self.value > 9:
      self.split()
      return True

    if self.value is not None:
      return False

    left_exploded = self.left.reduce_split(depth + 1)
    if left_exploded:
      return True
    return self.right.reduce_split(depth + 1)

  def run_all_reductions(self):
    while True:
      if not (self.reduce_explode(0) or self.reduce_split(0)):
        return

  def magnitude(self):
    if self.value is not None:
      return self.value
    return 3 * self.left.magnitude() + 2 * self.right.magnitude()


def build_tree(line, parent=None):
  root = Node(parent=parent)
  if not isinstance(line, list):
    root.value = line
  else:
    root.left = build_tree(line[0], parent=root)
    root.right = build_tree(line[1], parent=root)
  return root


def run():
  with open(SOURCE_FILE, 'r') as f:
    lines = [build_tree(json.loads(line.strip())) for line in f]

  root = lines[0]
  root.run_all_reductions()
  for line in lines[1:]:
    new_root = Node()
    new_root.left = root
    new_root.right = line
    root.parent = new_root
    line.parent = new_root
    root = new_root
    root.run_all_reductions()

  print(root.magnitude())


if __name__ == '__main__':
  run()
