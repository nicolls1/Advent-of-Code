import numpy as np
from scipy import signal

SOURCE_FILE = 'numbers.txt'
ENHANCEMENTS = 50
KEY_MATRIX = np.flipud(
  np.fliplr(
    np.array([
      [256, 128, 64],
      [32, 16, 8],
      [4, 2, 1],
    ])
  )
)


def enhance(image, image_alg, background):
  padded_image = np.pad(image, ((2, 2), (2, 2)), 'constant', constant_values=background)
  res = np.around(signal.fftconvolve(padded_image, KEY_MATRIX, mode='valid'))
  if background == 0:
    new_background = image_alg[0]
  else:
    new_background = image_alg[511]
  return [[image_alg[int(value)] for value in line] for line in res], new_background


def run():
  with open(SOURCE_FILE, 'r') as f:
    image_alg = [1 if char == '#' else 0 for char in f.readline().strip()]
    f.readline()

    image = []
    for line in f:
      image.append([1 if char == '#' else 0 for char in line.strip()])

  background = 0
  for _ in range(ENHANCEMENTS):
    image, background = enhance(image, image_alg, background)

  print(sum(sum(image, [])))


if __name__ == '__main__':
  run()
