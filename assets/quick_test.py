class Test():
    def __init__(self):
        self.grid = {}
        self.grid_start = (-200, 350) # (x, y) pos of leftmost, upper grid in mm
        self.grid_gap = abs(self.grid_start[0] * 2) / 11 # size of grid "square" in mm

        for x in range(12):
            for y in range(8):
                index = x * 8 + y - 16
                self.grid[index] = (self.grid_start[0] + x * self.grid_gap, self.grid_start[1] - y * self.grid_gap)

        for i in range(96):
            print(self.grid[i-16])

test = Test()

