import copy
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

SOURCE_FILE = 'd23/numbers.txt'
AMPHIPODS = ['A', 'B', 'C', 'D']
AMPHIPODS_SCORES = {
  'A': 1,
  'B': 10,
  'C': 100,
  'D': 1000
}
END_BURROW_X = {
  'A': 3,
  'B': 5,
  'C': 7,
  'D': 9
}


def distance(p1, p2):
  if p1.y == 1 or p2.y == 1:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
  else:
    intermediate = Position(p1.x, 1)
    return distance(p1, intermediate) + distance(intermediate, p2)


@dataclass
class Position:
  x: int
  y: int

  def get_key(self):
    return f'{self.x},{self.y}'

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y


@dataclass
class Node:
  position: Position
  amphipod: Any = None
  up: 'Node' = None
  right: 'Node' = None
  down: 'Node' = None
  left: 'Node' = None
  move_only: bool = None
  goal_amphipod: str = None

  def __repr__(self):
    return str((self.amphipod, self.position, self.move_only, self.goal_amphipod))

  def is_occupied(self):
    return self.amphipod is not None

  def get_neighbors(self):
    return [self.up, self.right, self.down, self.left]

  def can_node_travel_to_node(self, node):
    if (node.goal_amphipod is not None and node.goal_amphipod != self.amphipod) or \
        not node.is_below_finished() or \
        node.move_only:
      return False

    return self._can_travel(node, set())

  def _can_travel(self, node, visited):
    if self.position == node.position:
      return True
    for neighbor in self.get_neighbors():
      if neighbor is not None:
        new_visited = visited | {neighbor.position.get_key()}
        if neighbor.position.get_key() not in visited and \
            not neighbor.is_occupied():
          can_travel = neighbor._can_travel(node, new_visited)
          if can_travel:
            return True
    return False

  def is_below_finished(self):
    current = self.down
    while current is not None:
      if current.amphipod != current.goal_amphipod:
        return False
      current = current.down
    return True

  def __deepcopy__(self, memo={}):
    key = self.position.get_key()
    if key in memo:
      return memo[key]

    cls = self.__class__
    result = cls.__new__(cls)
    memo[self.position.get_key()] = result

    result.position = self.position
    result.amphipod = self.amphipod
    result.up = copy.deepcopy(self.up, memo)
    result.right = copy.deepcopy(self.right, memo)
    result.down = copy.deepcopy(self.down, memo)
    result.left = copy.deepcopy(self.left, memo)
    result.move_only = self.move_only
    result.goal_amphipod = self.goal_amphipod
    return result

  def print(self):
    return self.amphipod if self.amphipod is not None else '.'


class Board:
  def __init__(self, nodes, amphipod_end_positions):
    self.nodes = nodes
    self.amphipod_end_positions = amphipod_end_positions

  def add_node(self, node):
    self.nodes[node.position.get_key()] = node

  def get_node_at_position(self, position):
    return self.nodes.get(position.get_key())

  def get_amphipod_positions(self):
    nodes_with_amphipods = list(filter(lambda node: node.amphipod is not None, self.nodes.values()))
    return [(node.amphipod, node) for node in nodes_with_amphipods]

  def get_home_amphipods(self):
    remaining = []
    positions = self.get_amphipod_positions()
    for amphipod, node in positions:
      if (node.position not in self.amphipod_end_positions[amphipod] or
          (node.position in self.amphipod_end_positions[amphipod] and not node.is_below_finished())) and \
          node.goal_amphipod is not None:
        remaining.append((amphipod, node))
    return remaining

  def get_exited_amphipods(self):
    remaining = []
    positions = self.get_amphipod_positions()
    for amphipod, node in positions:
      if node.goal_amphipod is None or \
          node.amphipod != node.goal_amphipod or \
          not node.is_below_finished():
        remaining.append((amphipod, node))
    return remaining

  def is_end_position(self, position):
    return position.get_key() in self.amphipod_end_positions

  def get_goal_amphipod_for_position(self, position):
    if self.is_end_position():
      return next(amphipod for amphipod, positions in self.amphipod_end_positions if position in positions)
    return None

  def node_end_position(self, node):
    end_positions = self.amphipod_end_positions[node.amphipod]
    return next(
      (position for position in end_positions if
       node.can_node_travel_to_node(self.nodes[position.get_key()])),
      None)

  def is_finished(self):
    remaining = []
    positions = self.get_amphipod_positions()
    for amphipod, node in positions:
      if node.position not in self.amphipod_end_positions[amphipod]:
        remaining.append((amphipod, node))
    return len(remaining) == 0

  def get_open_nodes(self, amphipod):
    # just because position is open doesn't mean it is reachable
    open_nodes = []
    for node in self.nodes.values():
      if not node.move_only and not node.is_occupied() and (node.amphipod is None or node.goal_amphipod == amphipod):
        open_nodes.append(node)
    open_nodes.reverse()
    return open_nodes

  def print(self):
    print()
    for y in range(0, 5):
      line = ''
      for x in range(0, 13):
        pos = Position(x, y)
        if pos.get_key() in self.nodes.keys():
          line += self.nodes[pos.get_key()].print()
        else:
          line += '#'
      print(line)
    print()

  def __str__(self):
    ret = ''
    for y in range(1, 4):
      for x in range(1, 12):
        pos = Position(x, y)
        if pos.get_key() in self.nodes.keys():
          ret += self.nodes[pos.get_key()].print()
    return ret

  def __deepcopy__(self, memodict={}):
    new_nodes = {}
    for key, node in self.nodes.items():
      if key in memodict:
        new_nodes[key] = memodict[key]
        continue
      node_copy = copy.deepcopy(node, memodict)
      new_nodes[key] = node_copy
      memodict[key] = node_copy
    return Board(new_nodes, self.amphipod_end_positions)


def find_all_paths(board, out_paths, seen, prefix=[], depth=0):
  if board.is_finished():
    out_paths.append(prefix)
    return
  if depth == 12:
    return
  if depth == 1:
    print(depth)

  for amphipod, node in board.get_exited_amphipods():
    node_can_move_to_end_position = board.node_end_position(node)
    if node_can_move_to_end_position is not None and not (node_can_move_to_end_position == node.position):
      new_board = copy.deepcopy(board)
      new_board.nodes[node_can_move_to_end_position.get_key()].amphipod = node.amphipod
      new_board.nodes[node.position.get_key()].amphipod = None
      if str(depth) + str(new_board) not in seen:
        seen.add(str(depth) + str(board))
        find_all_paths(new_board, out_paths, seen,
                       [*prefix, (node.amphipod, node.position, node_can_move_to_end_position)],
                       depth + 1)
        return

  for amphipod, node in board.get_home_amphipods():
    for open_node in board.get_open_nodes(amphipod):
      if node.can_node_travel_to_node(open_node):
        new_board = copy.deepcopy(board)
        new_board.nodes[open_node.position.get_key()].amphipod = node.amphipod
        new_board.nodes[node.position.get_key()].amphipod = None
        if str(depth) + str(new_board) not in seen:
          seen.add(str(depth) + str(board))
          find_all_paths(new_board, out_paths, seen,
                         [*prefix, (node.amphipod, node.position, open_node.position)],
                         depth + 1)


def run():
  nodes = {}
  end_burrows_x_to_y = defaultdict(list)
  with open(SOURCE_FILE, 'r') as f:
    for y, line in enumerate(f):
      for x, char in enumerate(line):
        if char == '.':
          new_node = Node(position=Position(x, y))
          nodes[new_node.position.get_key()] = new_node
        if char in AMPHIPODS:
          new_node = Node(position=Position(x, y), amphipod=char)
          nodes[new_node.position.get_key()] = new_node
          end_burrows_x_to_y[x].append(y)
  amphipod_end_positions = {amphipod: [Position(x, y) for y in end_burrows_x_to_y[x]] for x, amphipod in
                            zip(sorted(end_burrows_x_to_y.keys()), AMPHIPODS)}

  for key, node in nodes.items():
    # fill neighbors
    node.up = nodes.get((Position(node.position.x, node.position.y - 1)).get_key())
    node.right = nodes.get((Position(node.position.x + 1, node.position.y)).get_key())
    node.down = nodes.get((Position(node.position.x, node.position.y + 1)).get_key())
    node.left = nodes.get((Position(node.position.x - 1, node.position.y)).get_key())
    node.move_only = node.position.x in end_burrows_x_to_y.keys() and \
                     node.position.y not in end_burrows_x_to_y[node.position.x]
    if node.position.get_key() in [position.get_key() for positions in amphipod_end_positions.values() for position in
                                   positions]:
      node.goal_amphipod = next(
        amphipod for amphipod, positions in amphipod_end_positions.items() if node.position in positions)

  board = Board(nodes, amphipod_end_positions)
  out_paths = []
  seen = set()
  find_all_paths(board, out_paths, seen=seen)
  print(min(
    [(sum([AMPHIPODS_SCORES[amphipod] * distance(start, end) for amphipod, start, end in path]), path) for path in
     out_paths], key=lambda x: x[0]))


if __name__ == '__main__':
  run()
