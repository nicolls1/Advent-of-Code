from __future__ import annotations

import re

SOURCE_FILE = 'numbers.txt'
MINUTES = 26
TIME_TO_OPEN_MINUTES = 1
TIME_TO_TRAVEL_MINUTES = 1


class Node:
  def __init__(self, name: str, rate: int):
    self.name = name
    self.rate = rate
    self.connections: list['Node'] = []

  def add_connection(self, new_connection: 'Node'):
    self.connections.append(new_connection)

  def __str__(self):
    return f'{self.name}@{self.rate}: {",".join([c.name for c in self.connections])}'


class State:
  def __init__(self, start: Node, minutes_remaining: int, total_flow: int, open_valves: set[str]):
    self.start = start
    self.minutes_remaining = minutes_remaining
    self.total_flow = total_flow
    self.open_valves = open_valves

  def __str__(self):
    return f'{self.start} {self.minutes_remaining} {self.total_flow} {self.open_valves}'


def get_next_states(state: State, non_zero_nodes: list[Node], travel_times: dict[str, dict[str, int]]):
  next_states: list[State] = []
  for node in non_zero_nodes:
    if node.name != state.start.name and node.name not in state.open_valves:
      minutes_remaining_at_connection = state.minutes_remaining - travel_times[state.start.name][node.name]
      if minutes_remaining_at_connection <= 0:
        next_states.append(State(state.start, 0, state.total_flow, state.open_valves.copy()))
        continue
      minutes_remaining_after_opening = minutes_remaining_at_connection - TIME_TO_OPEN_MINUTES
      current_open = state.open_valves.copy()
      current_open.add(node.name)
      updated_total_flow = state.total_flow + (minutes_remaining_after_opening) * node.rate
      next_states.append(State(node, minutes_remaining_after_opening, updated_total_flow, current_open))

  return next_states


def find_shortest_distance(start: Node, end: Node, traveled: int, visited: set[str]):
  if end.name in [c.name for c in start.connections]:
    return traveled + TIME_TO_TRAVEL_MINUTES

  all_paths = []
  for node in start.connections:
    if node.name in visited:
      continue
    new_visited = visited.copy()
    new_visited.add(node.name)
    distance = find_shortest_distance(node, end, traveled + TIME_TO_TRAVEL_MINUTES, new_visited)
    if distance is not None:
      all_paths.append(distance)

  if len(all_paths) == 0:
    return None

  return min(all_paths)


def run():
  nodes = {}
  node_connections = {}
  start = None
  max_pipe_flow = -1
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      match = re.match(r'Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)$', line.strip())
      name = match.groups()[0]
      rate = int(match.groups()[1])
      connections = match.groups()[2].split(', ')
      node = Node(name, rate)
      nodes[name] = node
      node_connections[name] = connections
      if name == 'AA':
        start = node
      if rate > max_pipe_flow:
        max_pipe_flow = rate

  for node_name, connections in node_connections.items():
    for connection_name in connections:
      nodes[node_name].add_connection(nodes[connection_name])

  non_zero_nodes = [node for node in nodes.values() if node.rate != 0]

  # shortest from any given node to any other node
  shortest_distances: dict[str, dict[str, int]] = {}
  for start_node in non_zero_nodes:
    shortest_distances[start_node.name] = {}
    for end_node in non_zero_nodes:
      if start_node.name != end_node.name:
        shortest_distances[start_node.name][end_node.name] = find_shortest_distance(start_node, end_node, 0, set())
  shortest_distances[start.name] = {}
  for node in non_zero_nodes:
    shortest_distances[start.name][node.name] = find_shortest_distance(start, node, 0, set())

  all_rates = [node.rate for node in nodes.values() if node.rate != 0]
  all_rates.sort(reverse=True)

  states = [State(start, MINUTES, 0, set())]
  end_states = []
  while len(states) > 0:
    current_state: State = states.pop()
    next_states = get_next_states(current_state, non_zero_nodes, shortest_distances)

    for next_state in next_states:
      if next_state.minutes_remaining == 0 or len(all_rates) == len(next_state.open_valves):
        # finished states
        end_states.append({'flow': next_state.total_flow, 'open_valves': next_state.open_valves})
      else:
        # continue exploring
        states.append(next_state)

  end_states.sort(key=lambda state: state['flow'], reverse=True)
  print(len(end_states), end_states[:10])
  max_combo_total = 0
  for idx, end_state1 in enumerate(end_states):
    if idx % 1000 == 0:
      print(idx)
    for end_state2 in end_states[idx:]:
      if len(end_state1['open_valves'].intersection(end_state2['open_valves'])) == 0:
        if end_state1['flow'] + end_state2['flow'] > max_combo_total:
          max_combo_total = end_state1['flow'] + end_state2['flow']
        break

  print(max_combo_total)


if __name__ == '__main__':
  run()
