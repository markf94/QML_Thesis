hilbert_map = {
    'a': {(0, 0): (0, 'd'), (0, 1): (1, 'a'), (1, 0): (3, 'b'), (1, 1): (2, 'a')},
    'b': {(0, 0): (2, 'b'), (0, 1): (1, 'b'), (1, 0): (3, 'a'), (1, 1): (0, 'c')},
    'c': {(0, 0): (2, 'c'), (0, 1): (3, 'd'), (1, 0): (1, 'c'), (1, 1): (0, 'b')},
    'd': {(0, 0): (0, 'a'), (0, 1): (3, 'c'), (1, 0): (1, 'd'), (1, 1): (2, 'd')},
}

def point_to_hilbert(x, y, order=16):
  current_square = 'a'
  position = 0
  for i in range(order - 1, -1, -1):
    position <<= 2
    quad_x = 1 if x & (1 << i) else 0
    quad_y = 1 if y & (1 << i) else 0
    quad_position, current_square = hilbert_map[current_square][(quad_x, quad_y)]
    position |= quad_position
  return position

p = point_to_hilbert(0,100,5);

print p
