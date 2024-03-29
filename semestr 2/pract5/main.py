import TKinter as tk
import math
import random
from copy import copy
from models import ImageInfo, SpaceShip, Sprite
from util import dist
from imagelogic import ImageStorage

WIDTH, HEIGHT = (800,) * 2
SCORE = 0
LIVES = 3
TIME = 0
GAME_STARTED = False


background = ImageStorage(
    ImageInfo([400, 400], [800, 800]), tk.load_image("./img/background.png")
)

frontground = ImageStorage(
    ImageInfo([400, 400], [800, 800]), tk.load_image("./img/frontground.png")
)

logo = ImageStorage(ImageInfo([200, 150], [400, 300]), tk.load_image("./img/logo.png"))

catship_img = ImageStorage(
    ImageInfo([45, 45], [90, 90], 35), tk.load_image("./img/ship.png")
)

bullet = ImageStorage(
    ImageInfo([5, 5], [10, 10], 3, 17), tk.load_image("./img/bullet.png")
)

asteroid = ImageStorage(
    ImageInfo([45, 45], [90, 90], 40), tk.load_image("./img/asteroid.png")
)

explosion = ImageStorage(
    ImageInfo([64, 64], [128, 128], 17, 24, True), tk.load_image("./img/explosion.png")
)


asteroidsgroup_set = set({})
bulletsgroup_set = set({})
explosionsgroup_set = set({})


def click(pos):
    """Обработка нажатия на начало игры"""
    global GAME_STARTED, LIVES, SCORE

    center = [WIDTH / 2, HEIGHT / 2]
    size = logo.info.size
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    if (not GAME_STARTED) and inwidth and inheight:
        GAME_STARTED = True
        LIVES = 3
        SCORE = 0


def asteroids_spawner():
    
    global asteroidsgroup_set, catship

    
    asteroid_sprite = Sprite(
        [random.choice(range(WIDTH)), random.choice(range(HEIGHT))],
        [random.randint(1, 3), random.randint(1, 3)],
        random.choice([-0.1, 0.1]),
        random.choice([-0.01, 0.01]),
        asteroid.image,
        asteroid.info,
    )

    
    if (
        len(asteroidsgroup_set) < 50
        and dist(asteroid_sprite.position, catship.position) > 200
        and GAME_STARTED
    ):
        asteroidsgroup_set.add(asteroid_sprite)


def draw(canvas):
    
    global TIME, SCORE, asteroidsgroup_set, LIVES, catship, bulletsgroup_set, GAME_STARTED

    
    TIME += 1
    wtime = (TIME / 2) % WIDTH
    center = frontground.info.center
    size = frontground.info.size

    
    canvas.draw_image(
        background.image,
        background.info.center,
        background.info.size,
        [WIDTH / 2, HEIGHT / 2],
        [WIDTH, HEIGHT],
    )

   
    canvas.draw_image(
        frontground.image,
        center,
        size,
        (wtime - WIDTH / 2, HEIGHT / 2),
        (WIDTH, HEIGHT),
    )
    canvas.draw_image(
        frontground.image,
        center,
        size,
        (wtime + WIDTH / 2, HEIGHT / 2),
        (WIDTH, HEIGHT),
    )

    # Статистика текущей игры
    str1 = "Счёт: " + str(SCORE)
    str2 = "Жизни: " + str(LIVES)
    canvas.draw_text(str(str2), [40, 40], 20, "white")
    canvas.draw_text(str(str1), [40, 80], 20, "white")

    
    catship.draw(canvas)

   
    catship.update()

    
    if LIVES <= 0:
        GAME_STARTED = False
        catship = SpaceShip(
            [WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_img.image, catship_img.info
        )
        catship.ismove = False

        
        for sprite in set(asteroidsgroup_set):
            asteroidsgroup_set.remove(sprite)

        for sprite in set(bulletsgroup_set):
            bulletsgroup_set.remove(sprite)

        for element in set(explosionsgroup_set):
            explosionsgroup_set.remove(element)

    
    if not GAME_STARTED:
       
        canvas.draw_image(
            logo.image,
            logo.info.center,
            logo.info.size,
            [WIDTH / 2, HEIGHT / 2],
            logo.info.size,
        )

   
    if GAME_STARTED:
        
        process_sprite_group(asteroidsgroup_set, canvas)
        process_sprite_group(bulletsgroup_set, canvas)
        process_sprite_group(explosionsgroup_set, canvas)

    
    if group_collide(asteroidsgroup_set, catship):
        LIVES -= 1
        catship.position = [HEIGHT / 2, WIDTH / 2]
        catship.vel = [0, 0]
        catship.angle = 0
        catship.angle_vel = 0
        catship.draw(canvas)
        catship.update()

    
    SCORE += group_group_collide(asteroidsgroup_set, bulletsgroup_set)


def process_sprite_group(group_set, canvas):
    
    for sprite in set(group_set):

        
        sprite.draw(canvas)

       
        if sprite.update():
            group_set.remove(sprite)


def group_collide(group_set, other_object):
    
    for sprite in set(group_set):

  
        if sprite.collide(other_object):
            group_set.remove(sprite)
            explosion_pos = sprite.position
            explosion_vel = [0, 0]
            explosion_avel = 0
       
            explosion_sprite = Sprite(
                explosion_pos,
                explosion_vel,
                0,
                explosion_avel,
                explosion.image,
                explosion.info,
            )
            
            explosionsgroup_set.add(explosion_sprite)
            return True

    return False


def group_group_collide(asteroids_set, bullets_set):


    counter = 0
    for sprite in copy(asteroids_set):

        if group_collide(bullets_set, sprite):
            asteroids_set.discard(sprite)
            counter += 1
    return counter


def keydown(button_id):

    global bulletsgroup_set

    if not GAME_STARTED:
        return

    # Поворот влево
    if button_id == 37 or button_id == 65:
        catship.incAv()

    # Поворот вправо
    if button_id == 39 or button_id == 68:
        catship.decAv()

    # Перемещение вперед
    if button_id == 38 or button_id == 87:
        catship.ismove = True

    # Выстрел
    if button_id == 32:
        bulletsgroup_set = catship.shoot(
            GAME_STARTED, bulletsgroup_set, bullet.image, bullet.info
        )


def keyup(button_id):

    if not GAME_STARTED:
        return


    if button_id == 37 or button_id == 39 or button_id == 65 or button_id == 68:
        catship.setAv()


    if button_id == 38 or button_id == 87:
        catship.ismove = False


localeframe = tk.create_frame("Практика 5. Астероиды", WIDTH, HEIGHT)
catship = SpaceShip(
    [WIDTH / 2, HEIGHT / 2], [0, 0], 0, catship_img.image, catship_img.info
)


localeframe.set_draw_handler(draw)
localeframe.set_keydown_handler(keydown)
localeframe.set_keyup_handler(keyup)
localeframe.set_mouseclick_handler(click)


timer = tk.create_timer(1000.0, asteroids_spawner)


timer.start()
localeframe.start()
