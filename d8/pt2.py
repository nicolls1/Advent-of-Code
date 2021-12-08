SOURCE_FILE = './numbers.txt'

# lengths
#  0: 6
#  1: 2
#  2: 5
#  3: 5
#  4: 4
#  5: 5
#  6: 6
#  7: 3
#  8: 7
#  9: 6

unique_lengths = {
  2: 1,
  3: 7,
  4: 4,
  7: 8,
}


# 1, 4, 7, 8 => length
# 0, 6, 9 => 6 not subset of 7, 9 subset of 4, 0 remaining
# 5 => subset of 6
# 2, 3 => 3 has all of 7 else 2

def find_numbers(inputs):
  number_to_symbols = {}
  remaining_inputs = set()
  # by unique lengths
  for input in inputs:
    if len(input) in unique_lengths.keys():
      number_to_symbols[unique_lengths[len(input)]] = input
    else:
      remaining_inputs.add(input)

  # length 6 combos
  length_six = set(filter(lambda input: len(input) == 6, remaining_inputs))
  six = next((x for x in length_six if not set(x) >= set(number_to_symbols[7])))
  number_to_symbols[6] = six
  remaining_inputs.remove(six)
  length_six.remove(six)

  nine = next((x for x in length_six if set(x) >= set(number_to_symbols[4])))
  number_to_symbols[9] = nine
  remaining_inputs.remove(nine)
  length_six.remove(nine)

  zero = length_six.pop()
  number_to_symbols[0] = zero
  remaining_inputs.remove(zero)

  # remaining
  five = next((x for x in remaining_inputs if set(x) <= set(number_to_symbols[6])))
  number_to_symbols[5] = five
  remaining_inputs.remove(five)

  three = next((x for x in remaining_inputs if set(x) >= set(number_to_symbols[7])))
  number_to_symbols[3] = three
  remaining_inputs.remove(three)

  number_to_symbols[2] = remaining_inputs.pop()

  return {symbols: number for number, symbols in number_to_symbols.items()}


def get_symbol_number(symbols_to_number, symbol):
  for symbol_key, number in symbols_to_number.items():
    if set(symbol) == set(symbol_key):
      return number


def run():
  combinations = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      parts = line.strip().split('|')
      combinations.append({
        'inputs': parts[0].strip().split(' '),
        'outputs': parts[1].strip().split(' '),
      })

  out_sum = 0
  for combination in combinations:
    symbols_to_number = find_numbers(combination['inputs'])
    number = [str(get_symbol_number(symbols_to_number, output)) for output in combination['outputs']]
    out_sum += int(''.join(number))

  print(out_sum)


if __name__ == '__main__':
  run()
