from xbox360controller import Xbox360Controller

with Xbox360Controller(0, axis_threshold=0) as joy:
    joy.axis