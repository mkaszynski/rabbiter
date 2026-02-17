import pygame
import random
import os
import math
import time
import numpy as np
import pickle

IMAGE_PATH = "assets/"

world_name = input("World name: ")

pygame.init()

BLOCK_SIZE = 42

LENGTH, WIDTH = 100, 100


def abs2(value):
    if value < 0:
        value = 0
    return value


try:
    level = pickle.load(open(world_name + ".w", "rb"))[2]
except:
    level = 11 - abs2(int(input("hardness: 1 - 10: ")) - 1) + 1

# Set up the drawing window
screen = pygame.display.set_mode([40 * BLOCK_SIZE, 20 * BLOCK_SIZE])

AIR_BLOCK = 0
WATER_BLOCK = 1
FULL_PIPE_BLOCK = 2
CARROT_BLOCK = 3
WALL_BLOCK = 4
RABBIT_BLOCK = 5
SELLER_BLOCK = 6
BUYER_BLOCK = 7
INSERTER1_BLOCK = 8
INSERTER2_BLOCK = 9
INSERTER3_BLOCK = 10
TURRET_BLOCK = 11
BULLET_BLOCK = 12
TRAPPER_BLOCK = 13
AMMO_BLOCK = 14
PIPE_BLOCK = 15
CHICKEN_BLOCK = 16
FERTILIZER_BLOCK = 17
VAULT_BLOCK = 18
MONEY_BLOCK = 19
TRADER_BLOCK = 20
BOMB_BLOCK = 21
ARTILARY_BLOCK = 22
SHELL_BLOCK = 23
SHELL_BLOCK2 = 24

ignore = [
    WALL_BLOCK,
    TRAPPER_BLOCK,
    WALL_BLOCK,
    BOMB_BLOCK,
]


def add_line(screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


def perlin():
    imgx = LENGTH
    imgy = WIDTH  # image size
    octaves = int(math.log(max(imgx, imgy), 1.5))
    persistence = 0.7
    imgAr = [[0.0 for i in range(imgx)] for j in range(imgy)]  # image array
    totAmp = 0.0
    for k in range(octaves):
        freq = 2**k
        amp = persistence**k
        totAmp += amp
        # create an image from n by m grid of random numbers (w/ amplitude)
        # using Bilinear Interpolation
        n = freq + 1
        m = freq + 1  # grid size
        ar = [[random.random() * amp for i in range(n)] for j in range(m)]
        nx = imgx / (n - 1.0)
        ny = imgy / (m - 1.0)
        for ky in range(imgy):
            for kx in range(imgx):
                o = 0
                i = int(kx / nx)
                j = int(ky / ny)
                dx0 = kx - i * nx
                dx1 = nx - dx0
                dy0 = ky - j * ny
                dy1 = ny - dy0
                if int(imgAr[ky][kx] / totAmp * 255) - 10 > 128:
                    o += 1
                z = ar[j][i] * dx1 * dy1
                z += ar[j][i + 1] * dx0 * dy1
                z += ar[j + 1][i] * dx1 * dy0
                z += ar[j + 1][i + 1] * dx0 * dy0
                z /= nx * ny
                imgAr[ky][kx] += z  # add image layers together

    pick = []
    for i in range(imgy):
        pick.append([])
        for j in range(imgx):
            pick[i].append([])
    for ky in range(imgy):
        for kx in range(imgx):
            if int((imgAr[ky][kx] / totAmp * 255) * 0.9) < 120:
                pick[ky][kx] = int((imgAr[ky][kx] / totAmp * 255) * 0.9)
            else:
                pick[ky][kx] = int((imgAr[ky][kx] / totAmp * 255) * 0.9)
    return pick


font = pygame.font.Font("freesansbold.ttf", 20)

try:
    blocks = pickle.load(open(world_name + ".w", "rb"))[0]
except:
    area = perlin()
    blocks = []
    m = 0
    for i in area:
        for j in i:
            m += j
    m *= 1 / LENGTH / WIDTH
    for i in range(LENGTH):
        blocks.append([])
        for j in range(WIDTH):
            if area[j][i] > m - 20:
                blocks[i].append([i, j, AIR_BLOCK, 10000])
            else:
                blocks[i].append([i, j, WATER_BLOCK, 10000])


def rect_alpha(x, y, w, h, c):
    rect = pygame.Rect(x, y, w, h)
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, c, shape_surf.get_rect())
    screen.blit(shape_surf, rect)


labels = {
    AIR_BLOCK: "air",
    WATER_BLOCK: "water",
    FULL_PIPE_BLOCK: "full pipe",
    CARROT_BLOCK: "carrot",
    WALL_BLOCK: "wall",
    RABBIT_BLOCK: "rabbit",
    SELLER_BLOCK: "seller",
    BUYER_BLOCK: "buyer",
    INSERTER1_BLOCK: "inserter1",
    INSERTER2_BLOCK: "inserter2",
    INSERTER3_BLOCK: "inserter3",
    TURRET_BLOCK: "turret",
    BULLET_BLOCK: "bullet",
    TRAPPER_BLOCK: "trapper",
    AMMO_BLOCK: "ammo",
    PIPE_BLOCK: "pipe",
    CHICKEN_BLOCK: "chicken",
    FERTILIZER_BLOCK: "fertilizer",
    VAULT_BLOCK: "vault wall",
    MONEY_BLOCK: "money",
    TRADER_BLOCK: "trader",
    BOMB_BLOCK: "bomb",
    ARTILARY_BLOCK: "artilary",
    SHELL_BLOCK: "shell",
    SHELL_BLOCK2: "shell2",
}

colors = {
    AIR_BLOCK: (0, 150, 0),
    CARROT_BLOCK: (255, 128, 0),
    WALL_BLOCK: (100, 100, 100),
    RABBIT_BLOCK: (255, 128, 255),
    SELLER_BLOCK: (255, 200, 0),
    BUYER_BLOCK: (128, 100, 0),
    INSERTER1_BLOCK: (255, 0, 0),
    INSERTER2_BLOCK: (0, 255, 255),
    INSERTER3_BLOCK: (0, 255, 128),
    TURRET_BLOCK: (0, 0, 0),
    BULLET_BLOCK: (50, 150, 50),
    TRAPPER_BLOCK: (128, 64, 0),
    AMMO_BLOCK: (150, 150, 150),
    PIPE_BLOCK: (80, 80, 90),
    FULL_PIPE_BLOCK: (70, 70, 120),
    WATER_BLOCK: (0, 0, 255),
    CHICKEN_BLOCK: (255, 255, 255),
    FERTILIZER_BLOCK: (0, 80, 0),
    VAULT_BLOCK: (50, 50, 50),
    MONEY_BLOCK: (255, 200, 0),
    TRADER_BLOCK: (0, 255, 0),
    BOMB_BLOCK: (128, 100, 100),
    ARTILARY_BLOCK: (100, 100, 130),
    SHELL_BLOCK: (100, 75, 75),
    SHELL_BLOCK2: (100, 75, 75),
}

selection = {
    0: CARROT_BLOCK,
    1: WALL_BLOCK,
    2: SELLER_BLOCK,
    3: INSERTER1_BLOCK,
    4: INSERTER2_BLOCK,
    5: INSERTER3_BLOCK,
    6: BUYER_BLOCK,
    7: TURRET_BLOCK,
    8: TRAPPER_BLOCK,
    9: AMMO_BLOCK,
    10: PIPE_BLOCK,
    11: CHICKEN_BLOCK,
    12: FERTILIZER_BLOCK,
    13: VAULT_BLOCK,
    14: TRADER_BLOCK,
    15: BOMB_BLOCK,
}

cost = {
    CARROT_BLOCK: 4,
    WALL_BLOCK: 2,
    SELLER_BLOCK: 20,
    INSERTER1_BLOCK: 4,
    INSERTER2_BLOCK: 4,
    INSERTER3_BLOCK: 4,
    BUYER_BLOCK: 20,
    TURRET_BLOCK: 35,
    BULLET_BLOCK: 0,
    TRAPPER_BLOCK: 4,
    AMMO_BLOCK: 1,
    PIPE_BLOCK: 8,
    FULL_PIPE_BLOCK: 8,
    CHICKEN_BLOCK: 20,
    FERTILIZER_BLOCK: 2,
    VAULT_BLOCK: 50,
    MONEY_BLOCK: 5,
    TRADER_BLOCK: 20,
    BOMB_BLOCK: 25,
    ARTILARY_BLOCK: 60,
}

strength = {
    WALL_BLOCK: 0.975,
    SELLER_BLOCK: 0.5,
    BUYER_BLOCK: 0.7,
    INSERTER1_BLOCK: 0.7,
    INSERTER2_BLOCK: 0.7,
    INSERTER3_BLOCK: 0.7,
    TURRET_BLOCK: 0.95,
    TRAPPER_BLOCK: 0.7,
    AMMO_BLOCK: 0.4,
    PIPE_BLOCK: 0.6,
    FULL_PIPE_BLOCK: 0.6,
    CHICKEN_BLOCK: 0.5,
    FERTILIZER_BLOCK: 0,
    VAULT_BLOCK: 0.9975,
    MONEY_BLOCK: 0.5,
    TRADER_BLOCK: 0.5,
    BOMB_BLOCK: 0.9,
    ARTILARY_BLOCK: 0.99,
}

###############################################################################
# load all images
###############################################################################


def load_image(image_label):
    image_file = os.path.join(IMAGE_PATH, f"{image_label}.png")
    if not os.path.isfile(image_file):
        return None
    image = pygame.image.load(image_file).convert()
    image.set_colorkey((0, 0, 0))
    image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
    return image


images = {block_label: load_image(label) for block_label, label in labels.items()}

###############################################################################
select = 0

try:
    time1 = pickle.load(open(world_name + ".w", "rb"))[1]
except:
    time1 = -1000

try:
    money = pickle.load(open(world_name + ".w", "rb"))[3]
except:
    money = 40

try:
    hardness = pickle.load(open(world_name + ".w", "rb"))[4]
except:
    hardness = 0.99999

selection_held = False

loss = 0

posx, posy = 0, 0

scrollx, scrolly = 0, 0

###############################################################################
# Initialize block array
###############################################################################
# sized length x width with each item containing:
# - x location
# - y location
# - block type
# - rabbit priority value
data = np.zeros((LENGTH, WIDTH, 4), dtype=int)


def rand_change(rand, change):
    rand = 1 - rand
    rand = 1 / rand
    rand /= change
    rand = 1 / rand
    rand = 1 - rand
    return rand


tick_power = 3

###############################################################################
# Main application loop
###############################################################################
# Run until the user asks to quit
running = True
while running:
    # Fill the background with white
    screen.fill((0, 150, 0))
    pygame.event.poll()
    keys = pygame.key.get_pressed()
    mx, my = pygame.mouse.get_pos()
    mouse_held = pygame.mouse.get_pressed()

    timer = time.time()

    if keys[pygame.K_w]:
        scrolly -= 30
    if keys[pygame.K_s]:
        scrolly += 30
    if keys[pygame.K_a]:
        scrollx -= 30
    if keys[pygame.K_d]:
        scrollx += 30

    posx = scrollx * 0.25 + posx * 0.75
    posy = scrolly * 0.25 + posy * 0.75

    if scrollx < 0:
        scrollx = 0
    if scrolly < 0:
        scrolly = 0

    if scrollx > BLOCK_SIZE * LENGTH - 40 * BLOCK_SIZE:
        scrollx = BLOCK_SIZE * LENGTH - 40 * BLOCK_SIZE
    if scrolly > BLOCK_SIZE * WIDTH - 20 * BLOCK_SIZE:
        scrolly = BLOCK_SIZE * WIDTH - 20 * BLOCK_SIZE

    time1 += 1

    if time1 > 0:
        hardness = 1 / (1 - hardness)
        hardness *= 0.99975 + level * 0.00002
        hardness = 1 - 1 / hardness

    if not selection_held:
        if keys[pygame.K_e]:
            select = (select - 1) % len(selection)
            selection_held = True
        if keys[pygame.K_r]:
            select = (select + 1) % len(selection)
            selection_held = True

    if not keys[pygame.K_e] and not keys[pygame.K_r]:
        selection_held = False

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    updaterabbitmap = False
    if random.random() > 0.9:
        updaterabbitmap = True

    if mouse_held[0] or mouse_held[2] or keys[pygame.K_q]:
        for j in blocks:
            for i in j:
                if (
                    int((mx + posx) / BLOCK_SIZE) == i[0]
                    and int((my + posy) / BLOCK_SIZE) == i[1]
                    and i[2] == AIR_BLOCK
                    and mouse_held[0]
                ):
                    if money >= cost[selection[select]]:
                        money -= cost[selection[select]]
                        i[2] = selection[select]
                if (
                    int((mx + posx) / BLOCK_SIZE) == i[0]
                    and int((my + posy) / BLOCK_SIZE) == i[1]
                    and i[2] in cost
                    and time1 % 12 == 0
                    and mouse_held[0]
                ):
                    if i[2] != selection[select]:
                        if money >= cost[selection[select]]:
                            money += int(cost[i[2]] / 2)
                            money -= cost[selection[select]]
                            i[2] = selection[select]
                if i[2] in cost:
                    if mouse_held[2] and time1 % 12 == 0:
                        if (
                            int((mx + posx) / BLOCK_SIZE) == i[0]
                            and int((my + posy) / BLOCK_SIZE) == i[1]
                        ):
                            money += int(cost[i[2]] / 2)
                            i[2] = AIR_BLOCK
                if i[2] == WATER_BLOCK:
                    if mouse_held[2] and time1 % 12 == 0:
                        if (
                            int((mx + posx) / BLOCK_SIZE) == i[0]
                            and int((my + posy) / BLOCK_SIZE) == i[1]
                        ):
                            if money >= 40:
                                i[2] = AIR_BLOCK
                                money -= 40
                if keys[pygame.K_q]:
                    try:
                        if (
                            int((mx + posx) / BLOCK_SIZE) == i[0]
                            and int((my + posy) / BLOCK_SIZE) == i[1]
                        ):
                            mydic = {}
                            for m in selection.keys():
                                mydic.update({selection[m]: m})
                            select = mydic[i[2]]
                    except:
                        pass

    if time1 % tick_power == 0:
        for j in random.sample(blocks, len(blocks)):
            for i in random.sample(j, len(j)):
                if i[0] == 0 or i[0] == LENGTH - 2 or i[1] == 0 or i[1] == WIDTH - 2:
                    if random.random() > rand_change(hardness, tick_power):
                        if i[2] != WATER_BLOCK:
                            i[2] = RABBIT_BLOCK

                if i[2] == AIR_BLOCK:
                    continue

                if i[2] == CARROT_BLOCK:
                    try:
                        if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                            if random.random() > rand_change(0.9995, tick_power):
                                blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                        if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                            if random.random() > rand_change(0.9995, tick_power):
                                blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                        if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                            if random.random() > rand_change(0.9995, tick_power):
                                blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                        if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                            if random.random() > rand_change(0.9995, tick_power):
                                blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
                    except:
                        pass
                elif i[2] == RABBIT_BLOCK and random.random() > rand_change(
                    0.9, tick_power
                ):
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        if random.random() > 0.5:
                            u = random.choice(s)
                        else:
                            m = 100
                            for o in s:
                                if o[3] <= m:
                                    m = o[3]
                                    u = o
                            if m == 100:
                                u = random.choice(s)
                        if u[2] == AIR_BLOCK:
                            i[2] = AIR_BLOCK
                            blocks[u[0]][u[1]][2] = RABBIT_BLOCK
                        elif u[2] == CARROT_BLOCK or u[2] == CHICKEN_BLOCK:
                            loss += int(cost[blocks[u[0]][u[1]][2]] / 2)
                            if random.random() < 0.2:
                                blocks[u[0]][u[1]][2] = RABBIT_BLOCK
                            else:
                                blocks[u[0]][u[1]][2] = AIR_BLOCK
                        else:
                            if u[2] in strength:
                                if random.random() > strength[u[2]]:
                                    loss += int(cost[blocks[u[0]][u[1]][2]] / 2)
                                    i[2] = AIR_BLOCK
                                    blocks[u[0]][u[1]][2] = RABBIT_BLOCK
                        if random.random() > 0.999:
                            i[2] = AIR_BLOCK
                    except:
                        i[2] = AIR_BLOCK
                elif i[2] == SELLER_BLOCK:
                    try:
                        if blocks[i[0]][i[1] + 1][2] in cost:
                            money += int(cost[blocks[i[0]][i[1] + 1][2]] / 2)
                            blocks[i[0]][i[1] + 1][2] = AIR_BLOCK
                        if blocks[i[0]][i[1] - 1][2] in cost:
                            money += int(cost[blocks[i[0]][i[1] - 1][2]] / 2)
                            blocks[i[0]][i[1] - 1][2] = AIR_BLOCK
                        if blocks[i[0] + 1][i[1]][2] in cost:
                            money += int(cost[blocks[i[0] + 1][i[1]][2]] / 2)
                            blocks[i[0] + 1][i[1]][2] = AIR_BLOCK
                        if blocks[i[0] - 1][i[1]][2] in cost:
                            money += int(cost[blocks[i[0] - 1][i[1]][2]] / 2)
                            blocks[i[0] - 1][i[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == TRADER_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        o = random.choice(s)
                        if o[2] in cost:
                            p = []
                            p.append(blocks[i[0] - 1][i[1] + 1])
                            p.append(blocks[i[0] - 1][i[1] - 1])
                            p.append(blocks[i[0] + 1][i[1] + 1])
                            p.append(blocks[i[0] + 1][i[1] - 1])
                            b = random.choice(p)
                            if b[2] == AIR_BLOCK:
                                if cost[o[2]] >= 5:
                                    if random.random() < 5 / cost[o[2]]:
                                        blocks[o[0]][o[1]][2] = AIR_BLOCK
                                    blocks[b[0]][b[1]][2] = MONEY_BLOCK
                                else:
                                    if random.random() < cost[o[2]] / 5:
                                        blocks[b[0]][b[1]][2] = MONEY_BLOCK
                                    blocks[o[0]][o[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == INSERTER1_BLOCK:
                    try:
                        if random.random() > rand_change(0.7, tick_power):
                            l = random.choice([AIR_BLOCK, CARROT_BLOCK])
                            if (
                                blocks[i[0]][i[1] + 1][2] in cost
                                and blocks[i[0]][i[1] - 2][2] == l
                            ):
                                blocks[i[0]][i[1] - 2][2] = blocks[i[0]][i[1] + 1][2]
                                blocks[i[0]][i[1] + 1][2] = AIR_BLOCK
                            if (
                                blocks[i[0]][i[1] - 1][2] in cost
                                and blocks[i[0]][i[1] + 2][2] == l
                            ):
                                blocks[i[0]][i[1] + 2][2] = blocks[i[0]][i[1] - 1][2]
                                blocks[i[0]][i[1] - 1][2] = AIR_BLOCK
                            if (
                                blocks[i[0] + 1][i[1]][2] in cost
                                and blocks[i[0] - 2][i[1]][2] == l
                            ):
                                blocks[i[0] - 2][i[1]][2] = blocks[i[0] + 1][i[1]][2]
                                blocks[i[0] + 1][i[1]][2] = AIR_BLOCK
                            if (
                                blocks[i[0] - 1][i[1]][2] in cost
                                and blocks[i[0] + 2][i[1]][2] == l
                            ):
                                blocks[i[0] + 2][i[1]][2] = blocks[i[0] - 1][i[1]][2]
                                blocks[i[0] - 1][i[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == INSERTER2_BLOCK:
                    try:
                        if random.random() > rand_change(0.7, tick_power):
                            l = random.choice([AIR_BLOCK, CARROT_BLOCK])
                            if (
                                blocks[i[0]][i[1] - 2][2] in cost
                                and blocks[i[0]][i[1] - 1][2] == l
                            ):
                                blocks[i[0]][i[1] - 1][2] = blocks[i[0]][i[1] - 2][2]
                                blocks[i[0]][i[1] - 2][2] = AIR_BLOCK
                            if (
                                blocks[i[0]][i[1] + 2][2] in cost
                                and blocks[i[0]][i[1] + 1][2] == l
                            ):
                                blocks[i[0]][i[1] + 1][2] = blocks[i[0]][i[1] + 2][2]
                                blocks[i[0]][i[1] + 2][2] = AIR_BLOCK
                            if (
                                blocks[i[0] - 2][i[1]][2] in cost
                                and blocks[i[0] - 1][i[1]][2] == l
                            ):
                                blocks[i[0] - 1][i[1]][2] = blocks[i[0] - 2][i[1]][2]
                                blocks[i[0] - 2][i[1]][2] = AIR_BLOCK
                            if (
                                blocks[i[0] + 2][i[1]][2] in cost
                                and blocks[i[0] + 1][i[1]][2] == l
                            ):
                                blocks[i[0] + 1][i[1]][2] = blocks[i[0] + 2][i[1]][2]
                                blocks[i[0] + 2][i[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == INSERTER3_BLOCK:
                    try:
                        if random.random() > rand_change(0.7, tick_power):
                            s = []
                            s.append(blocks[i[0]][i[1] + 1])
                            s.append(blocks[i[0]][i[1] - 1])
                            s.append(blocks[i[0] - 1][i[1] + 1])
                            s.append(blocks[i[0] - 1][i[1] - 1])
                            s.append(blocks[i[0] + 1][i[1] + 1])
                            s.append(blocks[i[0] + 1][i[1] - 1])
                            s.append(blocks[i[0] + 1][i[1]])
                            s.append(blocks[i[0] - 1][i[1]])

                            m = []
                            for o in s:
                                if o[2] == AIR_BLOCK:
                                    m.append(o)

                            if m:
                                u = random.choice(m)
                                if blocks[i[0]][i[1] + 2][2] in cost and (
                                    u[2] == AIR_BLOCK or u[2] == CARROT_BLOCK
                                ):
                                    u[2] = blocks[i[0]][i[1] + 2][2]
                                    blocks[i[0]][i[1] + 2][2] = AIR_BLOCK
                                if blocks[i[0]][i[1] - 2][2] in cost and (
                                    u[2] == AIR_BLOCK or u[2] == CARROT_BLOCK
                                ):
                                    u[2] = blocks[i[0]][i[1] - 2][2]
                                    blocks[i[0]][i[1] - 2][2] = AIR_BLOCK
                                if blocks[i[0] + 2][i[1]][2] in cost and (
                                    u[2] == AIR_BLOCK or u[2] == CARROT_BLOCK
                                ):
                                    u[2] = blocks[i[0] + 2][i[1]][2]
                                    blocks[i[0] + 2][i[1]][2] = AIR_BLOCK
                                if blocks[i[0] - 2][i[1]][2] in cost and (
                                    u[2] == AIR_BLOCK or u[2] == CARROT_BLOCK
                                ):
                                    u[2] = blocks[i[0] - 2][i[1]][2]
                                    blocks[i[0] - 2][i[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == BUYER_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        o = random.choice(s)
                        if o[2] in cost:
                            p = []
                            p.append(blocks[i[0] - 1][i[1] + 1])
                            p.append(blocks[i[0] - 1][i[1] - 1])
                            p.append(blocks[i[0] + 1][i[1] + 1])
                            p.append(blocks[i[0] + 1][i[1] - 1])
                            b = random.choice(p)
                            m = random.choice(s)
                            if b[2] == MONEY_BLOCK and m[2] == AIR_BLOCK:
                                if cost[o[2]] >= 5:
                                    if random.random() < 5 / cost[o[2]]:
                                        blocks[m[0]][m[1]][2] = o[2]
                                    blocks[b[0]][b[1]][2] = AIR_BLOCK
                                else:
                                    if random.random() < cost[o[2]] / 5:
                                        blocks[b[0]][b[1]][2] = AIR_BLOCK
                                    blocks[m[0]][m[1]][2] = o[2]

                    except:
                        pass
                elif i[2] == TURRET_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        u = False
                        for o in s:
                            if o[2] == AMMO_BLOCK:
                                u = True

                        if u and random.random() > rand_change(0.95, tick_power):
                            if (
                                blocks[i[0]][i[1] + 1][2] == AIR_BLOCK
                                or blocks[i[0]][i[1] + 1][2] == AMMO_BLOCK
                            ):
                                blocks[i[0]][i[1] + 1][2] = BULLET_BLOCK
                            if (
                                blocks[i[0]][i[1] - 1][2] == AIR_BLOCK
                                or blocks[i[0]][i[1] - 1][2] == AMMO_BLOCK
                            ):
                                blocks[i[0]][i[1] - 1][2] = BULLET_BLOCK
                            if (
                                blocks[i[0] + 1][i[1]][2] == AIR_BLOCK
                                or blocks[i[0] + 1][i[1]][2] == AMMO_BLOCK
                            ):
                                blocks[i[0] + 1][i[1]][2] = BULLET_BLOCK
                            if (
                                blocks[i[0] - 1][i[1]][2] == AIR_BLOCK
                                or blocks[i[0] - 1][i[1]][2] == AMMO_BLOCK
                            ):
                                blocks[i[0] - 1][i[1]][2] = BULLET_BLOCK
                    except:
                        pass
                elif i[2] == BULLET_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        for u in s:
                            if u[2] == RABBIT_BLOCK:
                                blocks[u[0]][u[1]][2] = AIR_BLOCK
                                i[2] = AIR_BLOCK
                        if i[2] == BULLET_BLOCK:
                            u = random.choice(s)
                            if u[2] == AIR_BLOCK:
                                i[2] = AIR_BLOCK
                                blocks[u[0]][u[1]][2] = BULLET_BLOCK
                    except:
                        i[2] = AIR_BLOCK
                    if random.random() > rand_change(0.75, tick_power):
                        i[2] = AIR_BLOCK
                elif i[2] == TRAPPER_BLOCK:
                    try:
                        if random.random() > rand_change(0.97, tick_power):
                            if blocks[i[0]][i[1] + 1][2] == RABBIT_BLOCK:
                                blocks[i[0]][i[1] + 1][2] = AIR_BLOCK
                            if blocks[i[0]][i[1] - 1][2] == RABBIT_BLOCK:
                                blocks[i[0]][i[1] - 1][2] = AIR_BLOCK
                            if blocks[i[0] + 1][i[1]][2] == RABBIT_BLOCK:
                                blocks[i[0] + 1][i[1]][2] = AIR_BLOCK
                            if blocks[i[0] - 1][i[1]][2] == RABBIT_BLOCK:
                                blocks[i[0] - 1][i[1]][2] = AIR_BLOCK
                    except:
                        pass
                elif i[2] == PIPE_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] - 1][i[1] + 1])
                        s.append(blocks[i[0] - 1][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1] + 1])
                        s.append(blocks[i[0] + 1][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        random.shuffle(s)
                        for u in s:
                            if u[2] == FULL_PIPE_BLOCK and i[2] == PIPE_BLOCK:
                                i[2] = FULL_PIPE_BLOCK
                                blocks[u[0]][u[1]][2] = PIPE_BLOCK
                            if u[2] == WATER_BLOCK and random.random() > rand_change(
                                0.95, tick_power
                            ):
                                i[2] = FULL_PIPE_BLOCK
                    except:
                        pass
                elif i[2] == CHICKEN_BLOCK and random.random() > rand_change(
                    0.96, tick_power
                ):
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        u = random.choice(s)
                        if u[2] == AIR_BLOCK:
                            if random.random() < 0.9875:
                                i[2] = AIR_BLOCK
                                blocks[u[0]][u[1]][2] = CHICKEN_BLOCK
                            else:
                                i[2] = CHICKEN_BLOCK
                                blocks[u[0]][u[1]][2] = CHICKEN_BLOCK

                    except:
                        pass
                elif i[2] == BOMB_BLOCK:
                    s = []
                    s.append(blocks[i[0]][i[1] + 1])
                    s.append(blocks[i[0]][i[1] - 1])
                    s.append(blocks[i[0] - 1][i[1] + 1])
                    s.append(blocks[i[0] - 1][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1] + 1])
                    s.append(blocks[i[0] + 1][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1]])
                    s.append(blocks[i[0] - 1][i[1]])
                    w = False
                    for h in s:
                        if h[2] == BULLET_BLOCK or h[2] == RABBIT_BLOCK:
                            w = True
                    if w:
                        for h in s:
                            if h[2] == AIR_BLOCK or h[2] == RABBIT_BLOCK:
                                blocks[h[0]][h[1]][2] = BULLET_BLOCK
                        if random.random() > rand_change(0.95, tick_power):
                            i[2] = AIR_BLOCK
                elif i[2] == ARTILARY_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        for u in s:
                            if u[2] == AMMO_BLOCK:
                                blocks[u[0]][u[1]][2] = AIR_BLOCK
                                blocks[i[0] * 2 - u[0]][i[1] * 2 - u[1]][2] = (
                                    SHELL_BLOCK2
                                )
                                blocks[i[0] * 3 - u[0] * 2][i[1] * 3 - u[1] * 2][2] = (
                                    SHELL_BLOCK
                                )
                    except:
                        pass
                elif i[2] == SHELL_BLOCK and random.random() > 0.25:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        for u in s:
                            if u[2] == SHELL_BLOCK2:
                                if (
                                    blocks[i[0] * 2 - u[0]][i[1] * 2 - u[1]][2]
                                    != WATER_BLOCK
                                ):
                                    blocks[i[0] * 2 - u[0]][i[1] * 2 - u[1]][2] = (
                                        SHELL_BLOCK
                                    )
                                    i[2] = SHELL_BLOCK2
                                    blocks[u[0]][u[1]][2] = AIR_BLOCK
                                else:
                                    i[2] = AIR_BLOCK
                                    blocks[u[0]][u[1]][2] = AIR_BLOCK
                    except:
                        i[2] = AIR_BLOCK
                elif i[2] == SHELL_BLOCK2:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        s.append(blocks[i[0]][i[1] + 2])
                        s.append(blocks[i[0]][i[1] - 2])
                        s.append(blocks[i[0] + 2][i[1]])
                        s.append(blocks[i[0] - 2][i[1]])
                        if random.random() > 0.99:
                            i[2] = AIR_BLOCK
                    except:
                        i[2] = AIR_BLOCK
                elif i[2] == SHELL_BLOCK:
                    try:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        s.append(blocks[i[0]][i[1] + 2])
                        s.append(blocks[i[0]][i[1] - 2])
                        s.append(blocks[i[0] + 2][i[1]])
                        s.append(blocks[i[0] - 2][i[1]])
                        if random.random() > 0.99:
                            i[2] = AIR_BLOCK

                    except:
                        i[2] = AIR_BLOCK

                try:
                    if i[2] == CARROT_BLOCK:
                        s = []
                        s.append(blocks[i[0]][i[1] + 1])
                        s.append(blocks[i[0]][i[1] - 1])
                        s.append(blocks[i[0] - 1][i[1] + 1])
                        s.append(blocks[i[0] - 1][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1] + 1])
                        s.append(blocks[i[0] + 1][i[1] - 1])
                        s.append(blocks[i[0] + 1][i[1]])
                        s.append(blocks[i[0] - 1][i[1]])
                        for o in s:
                            if o[2] == FULL_PIPE_BLOCK:
                                if random.random() > rand_change(0.9985, tick_power):
                                    blocks[o[0]][o[1]][2] = PIPE_BLOCK
                                if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                                if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                                if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                                if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
                            if o[2] == FERTILIZER_BLOCK:
                                if random.random() > rand_change(0.9993, tick_power):
                                    blocks[o[0]][o[1]][2] = AIR_BLOCK
                                if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                                if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                                if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                                if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                                    if random.random() > rand_change(
                                        0.9975, tick_power
                                    ):
                                        blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
                except:
                    pass

    if updaterabbitmap:
        for j in blocks:
            for i in j:
                if (
                    i[2] != WATER_BLOCK
                    and 0 < i[0] < len(blocks) - 1
                    and 0 < i[1] < len(blocks) - 1
                ):
                    s = []
                    s.append(blocks[i[0]][i[1] + 1])
                    s.append(blocks[i[0]][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1]])
                    s.append(blocks[i[0] - 1][i[1]])
                    m = 1000
                    for u in s:
                        if u[3] <= m:
                            m = u[3]
                    if not m == 1000:
                        i[3] = m + 1
                if i[2] in cost and i[2] not in ignore:
                    i[3] = 0

    for j in blocks:
        for i in j:
            image = images[i[2]]
            if image:
                rect = image.get_rect()
                rect.center = (
                    i[0] * BLOCK_SIZE + BLOCK_SIZE / 2 - posx,
                    i[1] * BLOCK_SIZE + BLOCK_SIZE / 2 - posy,
                )
                screen.blit(image, rect)
            else:
                map1 = pygame.Rect(
                    i[0] * BLOCK_SIZE - posx,
                    i[1] * BLOCK_SIZE - posy,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, colors[i[2]], map1)

            if (
                int((mx + posx) / BLOCK_SIZE) == i[0]
                and int((my + posy) / BLOCK_SIZE) == i[1]
            ):
                rect_alpha(
                    i[0] * BLOCK_SIZE - posx,
                    i[1] * BLOCK_SIZE - posy,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                    (
                        colors[selection[select]][0],
                        colors[selection[select]][1],
                        colors[selection[select]][2],
                        128,
                    ),
                )

    for i in selection.keys():
        image = images[selection[i]]
        if image:
            if select == i:
                rect_alpha(
                    i * 80 + 195 - BLOCK_SIZE / 2,
                    795 - BLOCK_SIZE / 2,
                    BLOCK_SIZE + 10,
                    BLOCK_SIZE + 10,
                    colors[selection[i]],
                )

            rect = image.get_rect()
            rect.center = (
                i * 80 + 200,
                800,
            )
            screen.blit(image, rect)

    timer = time.time() - timer

    add_line(screen, f"fps: {1 / timer:.0f}", 700, 0)

    clock = pygame.time.Clock()
    clock.tick(60)

    add_line(
        screen,
        "selected block: "
        + labels[selection[select]]
        + " cost: "
        + str(cost[selection[select]]),
        0,
        0,
    )
    add_line(screen, "money: " + str(int(money)), 0, 30)
    if time1 < 1:
        add_line(screen, f"No rabbits spawning for {-time1 / 28:.1f} seconds", 0, 60)
    else:
        add_line(
            screen,
            f"rabbit spawning every {1 / (1 - (hardness) ** 180) / 7:.2f} seconds",
            0,
            60,
        )

    add_line(screen, f"loss of money from the rabbits: {loss:.0f}", 0, 90)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

pickle.dump([blocks, time1, level, money, hardness], open(world_name + ".w", "wb"))
