import random as rand

class Dice:
    def __init__(self, sides: int):
        if(sides < 2):
           raise ValueError("Die must have more than 2 sides to be valid.") 
        self.sides = sides

    def roll(self):
        res = rand.randint(1,self.sides)
        return res

    def rolls(self, times: int):
        res = []
        for i in range(times):
            res.append(rand.randint(1,self.sides))
        return res