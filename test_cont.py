from xbox360controller import Xbox360Controller

with Xbox360Controller(0, axis_threshold=0) as joy:
  while True:
    l_x = int(joy.axis_l.x)
    l_y = int(joy.axis_l.y)
    l_x *= 10
    l_y *= 10
    print(l_x, l_y)
