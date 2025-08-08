from xbox360controller import Xbox360Controller

with Xbox360Controller(0, axis_threshold=0) as joy:
  while True:
#    l_x = 0.5 - joy.axis_l.x
#    l_y = 0.5 + joy.axis_l.y
    l_x *= 10
    l_y *= 10
    print(l_y, l_x)
