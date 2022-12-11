import math
import re

SOURCE_FILE = 'numbers.txt'

ROUNDS = 10000

OPERATIONS = {
  '*': math.prod,
  '+': sum,
}


def get_operation_input_value(operation_input: str, item: int):
  return item if not operation_input.isdigit() else int(operation_input)


def run_operation(items: list[int], operation, monkey_test_numbers: list[int]):
  return [OPERATIONS[operation[1]]([get_operation_input_value(operation[0], item),
                                    get_operation_input_value(operation[2], item)]) % monkey_test_numbers[idx] for
          idx, item in enumerate(items)]


def run_round(monkeys, monkey_touch_counts: list[int], monkey_test_numbers: list[int]):
  for idx, monkey in enumerate(monkeys):
    for item in monkey['items']:
      monkey_touch_counts[idx] = monkey_touch_counts[idx] + 1
      new_item_worry = run_operation(item, monkey['operation'], monkey_test_numbers)
      if new_item_worry[idx] == 0:
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
  monkey_test_numbers = [monkey['test'] for monkey in monkeys]

  # replace item worries with a list of remainders
  for monkey in monkeys:
    new_items = []
    for item in monkey['items']:
      new_items.append([item % test_number for test_number in monkey_test_numbers])
    monkey['items'] = new_items

  for _ in range(ROUNDS):
    run_round(monkeys, monkey_touch_counts, monkey_test_numbers)
  monkey_touch_counts.sort(reverse=True)
  print('monkey business', math.prod(monkey_touch_counts[:2]))


if __name__ == '__main__':
  run()
