import math
import re

SOURCE_FILE = 'numbers.txt'

ROUNDS = 20
RELIEF_FACTOR = 3

OPERATIONS = {
  '*': math.prod,
  '+': sum,
}


def get_operation_input_value(operation_input: str, item: int):
  return item if not operation_input.isdigit() else int(operation_input)


def run_operation(item: int, operation):
  return OPERATIONS[operation[1]]([get_operation_input_value(operation[0], item),
                                   get_operation_input_value(operation[2], item)])


def run_round(monkeys, monkey_touch_counts: list[int]):
  for idx, monkey in enumerate(monkeys):
    for item in monkey['items']:
      monkey_touch_counts[idx] = monkey_touch_counts[idx] + 1
      new_item_worry = math.floor(run_operation(item, monkey['operation']) / RELIEF_FACTOR)
      if new_item_worry % monkey['test'] == 0:
        monkeys[monkey['true_destination']]['items'].append(new_item_worry)
      else:
        monkeys[monkey['false_destination']]['items'].append(new_item_worry)
    monkey['items'] = []


def run():
  monkeys = []
  with open(SOURCE_FILE, 'r') as f:
    while True:
      _monkey = f.readline()
      items = [int(item) for item in f.readline().split(':')[1].strip().split(', ')]
      operation = re.match(r'Operation: new = (.*) ([\*\+]) (.*)', f.readline().strip()).groups()
      test = int(f.readline().split(' ')[-1])
      true_destination = int(f.readline().split(' ')[-1])
      false_destination = int(f.readline().split(' ')[-1])

      monkeys.append({
        'items': items,
        'operation': operation,
        'test': test,
        'true_destination': true_destination,
        'false_destination': false_destination,
      })

      if len(f.readline()) == 0:
        break

  monkey_touch_counts = [0 for _ in range(len(monkeys))]

  for _ in range(ROUNDS):
    run_round(monkeys, monkey_touch_counts)
  monkey_touch_counts.sort(reverse=True)
  print('monkey business', math.prod(monkey_touch_counts[:2]))


if __name__ == '__main__':
  run()
