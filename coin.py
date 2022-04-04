class coin:
    def __init__(self, x, y, collided, not_dealt):
        self.x = x
        self.y = y
        self.collided = collided
        self.not_dealt = not_dealt
        
class coins:
    def __init__(self):
        self.coins_list = []
        
    def addToList(self, x, w, step1, y, h, step2):
        for i in range(x, x + w, step1):
            for j in range(y, y + h, step2):
                self.coins_list.append(coin(i, j, False, True))