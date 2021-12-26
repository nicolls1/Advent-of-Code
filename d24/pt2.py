import math

SOURCE_FILE = 'numbers.txt'

'''
ADD_X_VALUE = [10, 12, 13, 13, 14, -2, 11, -15, -10, 10, -10, -4, -1, -1]
ADD_Y_VALUE = [ 0,  6,  4,  2,  9,  1, 10,   6,   4,  6,   3,  9, 15,  5]

push input[0] + 0
push input[1] + 6
push input[2] + 4
push input[3] + 2
push input[4] + 9
pop  input[5] == pop - 2
push input[6] + 10
pop  input[7] == pop - 15
pop  input[8] == pop - 10
push input[9] + 6
pop  input[10] == pop - 10
pop  input[11] == pop - 4
pop  input[12] == pop - 1
pop  input[13] == pop - 1

input[5] == input[4] + 7
input[7] == input[6] - 5
input[8] == input[3] - 8
input[10] == input[9] - 4
input[11] == input[2]
input[12] == input[1] + 5
input[13] == input[0] - 1

          1111
01234567890123
--------------
21191861151161
'''


def div(a, b):
  result = a / b
  return math.floor(result) if result > 0 else math.ceil(result)


def get_input_values(operation_inputs, registers):
  inputs = []
  for operation_input in operation_inputs:
    try:
      inputs.append(int(operation_input))
    except:
      inputs.append(registers[operation_input])
  return inputs


class ALU:
  def operations_definition(self):
    return {
      'inp': lambda a: self.get_next_input(),
      'add': lambda a, b: a + b,
      'mul': lambda a, b: a * b,
      'div': div,
      'mod': lambda a, b: a % b,
      'eql': lambda a, b: 1 if a == b else 0
    }

  def __init__(self, operations):
    self.operations = operations
    self.input_index = 0
    self.inputs = None

  def get_next_input(self):
    next_input = self.inputs[self.input_index]
    self.input_index += 1
    return next_input

  def run(self, inputs):
    self.inputs = inputs
    registers = {
      'w': 0,
      'x': 0,
      'y': 0,
      'z': 0,
    }
    for operation in self.operations:
      registers[operation[1]] = self.operations_definition()[operation[0]](
        *get_input_values(operation[1:], registers))
    return registers


def run():
  operations = []
  with open(SOURCE_FILE, 'r') as f:
    for line in f:
      operations.append(line.strip().split(' '))

  alu = ALU(operations)
  print(alu.run([2, 1, 1, 9, 1, 8, 6, 1, 1, 5, 1, 1, 6, 1]))


if __name__ == '__main__':
  run()
