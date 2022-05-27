import pygame
from random import randrange

win = 1000
Snake_Size = 50
Apple_Size = 20

x, y = randrange(0, win, Snake_Size ), randrange(0, win, Snake_Size)
apple = randrange(0, win, Snake_Size),randrange(0, win, Snake_Size)
lenght = 1
snake = [(x, y)]
dx, dy = 0, 0
fps = 5

pygame.init()
sc = pygame.display.set_mode([win, win])
clock = pygame.time.Clock()
while True:
    sc.fill(pygame.Color('black'))
    #змея
    [(pygame.draw.rect(sc, pygame.Color('red'),(i, j, Snake_Size, Snake_Size))) for i, j in snake]
    #яблоко
    pygame.draw.rect(sc, pygame.Color("Yellow"), (*apple, Snake_Size, Snake_Size ))
    #движение змеи
    x += dx * Snake_Size
    y += dy * Snake_Size
    snake.append((x, y))
    #ограничение размера змеи по её длине
    snake = snake[-lenght:]
    #съедание яблока
    if snake[-1] == apple:
        apple = randrange(0, win, Snake_Size),randrange(0, win, Snake_Size)
        lenght += 1
        fps += 1
    #game over
    if x < -100 or x > 1100 or y < -100 or y > 1100:
        print("GAME OVER")
        break
    if len(snake)!= len(set(snake)):
        print("GAME OVER")
        break
    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        dx, dy = 0, -1
    if key[pygame.K_s]:
        dx, dy = 0, 1
    if key[pygame.K_d]:
        dx, dy = 1, 0
    if key[pygame.K_a]:
        dx, dy = -1, 0
        