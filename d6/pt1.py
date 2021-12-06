from collections import defaultdict

SOURCE_FILE = './numbers.txt'
RUN_DAYS = 80
FIRST_SPAWN_TIME = 8
REST_SPAWN_TIME = 6


def get_next_day(age_counts):
  next_age_counts = defaultdict(int)
  for age, count in age_counts.items():
    if age == 0:
      next_age_counts[REST_SPAWN_TIME] += count
      next_age_counts[FIRST_SPAWN_TIME] += count
    else:
      next_age_counts[age - 1] += count
  return next_age_counts


def run():
  with open(SOURCE_FILE, 'r') as f:
    fish_age_list = [int(age) for age in f.readline().strip().split(',')]

  age_counts = defaultdict(int)
  for age in fish_age_list:
    age_counts[age] += 1

  for _ in range(RUN_DAYS):
    age_counts = get_next_day(age_counts)

  print(sum(age_counts.values()))


if __name__ == '__main__':
  run()
