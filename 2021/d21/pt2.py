SOURCE_FILE = 'numbers.txt'
WINNING_SCORE = 21
THREE_ROLLS_SUMS = {
  3: 1,  # 111
  4: 3,  # 112, 121, 211
  5: 6,  # 113, 131, 311, 122, 221, 212
  6: 7,  # 123, 132, 222, 213, 312, 321, 132
  7: 6,  # 133, 313, 331, 223, 232, 322
  8: 3,  # 332, 323, 233
  9: 1  # 333
}


def get_cache_key(scores, positions, p1_turn):
  return ','.join([str(value) for value in [*scores, *positions, str(p1_turn)]])


def find_winner(scores, positions, p1_turn, cache):
  if scores[0] >= WINNING_SCORE:
    return [1, 0]
  if scores[1] >= WINNING_SCORE:
    return [0, 1]
  if get_cache_key(scores, positions, p1_turn) in cache:
    return cache[get_cache_key(scores, positions, p1_turn)]

  winner_universes = [0, 0]
  for key in THREE_ROLLS_SUMS.keys():
    current_positions = [*positions]
    current_scores = [*scores]
    update_key = 0 if p1_turn else 1
    total = current_positions[update_key] + key
    current_positions[update_key] = total % 10 if total % 10 != 0 else 10
    current_scores[update_key] += current_positions[update_key]
    universes = find_winner(current_scores, current_positions, not p1_turn, cache)
    winner_universes = [
      (universe * THREE_ROLLS_SUMS[key]) + winner_universes[idx]
      for idx, universe in enumerate(universes)
    ]
  cache[get_cache_key(scores, positions, p1_turn)] = winner_universes
  return winner_universes


def run():
  with open(SOURCE_FILE, 'r') as f:
    p1_position = int(f.readline().strip().split(' ')[-1])
    p2_position = int(f.readline().strip().split(' ')[-1])

  cache = {}
  print(max(find_winner([0, 0], [p1_position, p2_position], True, cache)))


if __name__ == '__main__':
  run()
