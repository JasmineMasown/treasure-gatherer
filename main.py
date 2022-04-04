import pygame
import coin
import tree

from pygame import mixer

pygame.init()

surface1 = pygame.display.set_mode((500,600))
pygame.display.set_caption("Treasure Gatherer")
pygame.display.set_icon(pygame.image.load("Resources/Images/Treasure-icon.png"))

boy_img = pygame.image.load("Resources/Images/boy.png")
tree_img = pygame.image.load("Resources/Images/tree.png")
coin_img = pygame.image.load("Resources/Images/coin.png")

mixer.music.load("Resources/music/Victory 1.wav")
mixer.music.play(-1)

# drawing items
class items_set:
    def __init__(self, x, w, step1, y, h, step2, img):
        self.x = x
        self.w = w
        self.step1 = step1
        self.y = y
        self.h = h
        self.step2 = step2
        self.img = img

    def draw_items(self):
        for x in range(self.x, self.x + self.w, self.step1):
            for y in range(self.y, self.y + self.h, self.step2):
                if self.img == "Resources/Images/tree.png":
                    tree_set.append(tree.tree(x,y))

                surface1.blit(pygame.image.load(self.img), (x, y))

trees_obj = tree.trees()
trees_obj.addToList(50, 400, 100, 60, 200, 100)
trees_obj.addToList(100, 300, 90, 110, 300, 120)

trees_list = trees_obj.trees_list

coins_obj = coin.coins()
coins_obj.addToList(100, 400, 100, 60, 200, 100)
coins_obj.addToList(50, 400, 50, 280, 40, 40)
coins_obj.addToList(50, 400, 90, 230, 200, 120)

coins_list = coins_obj.coins_list

# boy
x,y = (240, 410)
changeX, changeY = (0,0)

def draw_boy():
    surface1.blit(boy_img, (x,y))

# collision detection: boy and item :- x, y, 33, 35
def collision_detection(itemX, itemY, object):
    if object == "COIN":
        return ((itemX + 32 >= x >= itemX) or (itemX + 32 >= x + 33 >= itemX)) and ((itemY + 32 >= y >= itemY) or (itemY + 32 >= y + 35 >= itemY))
    if object == "TREE":
        return ((itemX + 32 >= x >= itemX) or (itemX + 32 >= x + 33 >= itemX)) and ((itemY + 32 >= y >= itemY + 10) or (itemY + 32 >= y + 35 >= itemY + 10))

# score
score = 0

font = pygame.font.Font("Resources/Fonts/OriginTech.otf", 33)
textX = x + 55
textY = y + 100

def show_score():
    score_font = font.render("Score : " + str(score), True, (244, 221, 73))
    surface1.blit(score_font, (textX, textY))

lives = 5
livesX = 40
livesY = textY


def show_lives():
    lives_font = font.render("Lives : " + str(lives), True, (255, 0, 0))
    surface1.blit(lives_font, (livesX, livesY))

count = 0

# game-loop
gameOn = True
while gameOn:
    # event-handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                changeY = -2
            if event.key == pygame.K_DOWN:
                changeY = 2
            if event.key == pygame.K_LEFT:
                changeX = -2
            if event.key == pygame.K_RIGHT:
                changeX = 2

        if event.type == pygame.KEYUP:
            changeY = 0
            changeX = 0

    # update
    x += changeX
    y += changeY

    if x <= 40:
        x = 40
    elif x >= 460 - 33:
        x = 460 - 33

    if y <= 40:
        y = 40
    elif y >= 460 - 35:
        y = 460 - 35

    for c in coins_list:
        if collision_detection(c.x, c.y, "COIN"):
            c.collided = True

        if c.collided and c.not_dealt:
            score += 10
            count += 1

            print(score)
            coins_list.remove(c)

    for t in trees_list:
        if collision_detection(t.x, t.y, "TREE"):
            t.collided = True
        else:
            t.collided = False

        if t.collided and t.not_dealt:
            score -= 5
            lives -= 1
            print(score)
            if collision_detection(t.x, t.y, "TREE"):
                t.not_dealt = False
        elif not t.collided:
            t.not_dealt = True

    if count >= 5:
        lives += 1
        count = 0


    # draw
    pygame.draw.rect(surface1, (0, 0, 0), pygame.Rect(0, 0, 500, 600))
    pygame.draw.rect(surface1, (111,157,0), pygame.Rect(40,40,420,420))
    for t in trees_list:
        surface1.blit(tree_img, (t.x, t.y))
    for c in coins_list:
        surface1.blit(coin_img, (c.x, c.y))
    draw_boy()
    show_score()
    show_lives()

    if lives <= 0:
       new_font = pygame.font.Font("Resources/Fonts/OriginTech.otf", 50)
       show_font = new_font.render("Game Over", True, (244, 221, 73))
       surface1.blit(show_font, (100, 250))
       gameOn = False

    # display
    pygame.display.flip()