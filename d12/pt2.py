from collections import defaultdict

SOURCE_FILE = 'numbers.txt'


def find_end_path(nodes, visited, current_value, duplicate_small_available):
  scoped_visited = [*visited, current_value]
  if current_value == 'end':
    return [','.join(scoped_visited)]

  found_paths = []
  for connection in nodes[current_value]:
    if not connection == 'start':
      child_paths = None
      if connection.isupper() or connection not in scoped_visited:
        child_paths = find_end_path(nodes, scoped_visited, connection, duplicate_small_available)
      elif connection in scoped_visited and duplicate_small_available:
        child_paths = find_end_path(nodes, scoped_visited, connection, False)
      if child_paths:
        found_paths += child_paths
  return found_paths


def run():
  nodes = defaultdict(list)
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      start_node, end_node = line.strip().split('-')
      nodes[start_node].append(end_node)
      nodes[end_node].append(start_node)

  paths = find_end_path(nodes, [], 'start', True)
  print(len(paths))


if __name__ == '__main__':
  run()
