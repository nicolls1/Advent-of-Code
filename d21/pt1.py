SOURCE_FILE = 'numbers.txt'
WINNING_SCORE = 1000


class Die:
  def __init__(self):
    self.last_roll = 0
    self.roll_count = 0

  def roll(self):
    self.roll_count += 1
    self.last_roll = max(((self.last_roll + 1) % 101), 1)
    return self.last_roll


def run():
  with open(SOURCE_FILE, 'r') as f:
    p1_position = int(f.readline().strip().split(' ')[-1])
    p2_position = int(f.readline().strip().split(' ')[-1])

  die = Die()
  p1_score = 0
  p2_score = 0
  p1_turn = True
  while p1_score < WINNING_SCORE and p2_score < WINNING_SCORE:
    move_spaces = sum(die.roll() for i in range(3))
    if p1_turn:
      total = p1_position + move_spaces
      p1_position = total % 10 if total % 10 != 0 else 10
      p1_score += p1_position
    else:
      total = p2_position + move_spaces
      p2_position = total % 10 if total % 10 != 0 else 10
      p2_score += p2_position
    p1_turn = not p1_turn
  if p1_score >= WINNING_SCORE:
    loser_score = p2_score
  else:
    loser_score = p1_score
  print(die.roll_count * loser_score)


if __name__ == '__main__':
  run()
