import pygame
import random
import os
import math
import time
import numpy as np

IMAGE_PATH = '/home/michael/coding/python/games/rabbiter/'

pygame.init()

BLOCK_SIZE = 28

# Set up the drawing window
screen = pygame.display.set_mode([60 * BLOCK_SIZE, 30 * BLOCK_SIZE])


def add_line(screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, (50, 50, 50))
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


def perlin():
    imgx = 60
    imgy = 30  # image size
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

blocks = []

area = perlin()

m = 0

for i in area:
    for j in i:
        m += j

length, width = 60, 30
m *= 1 / length / width



def rect_alpha(x, y, w, h, c):
    rect = pygame.Rect(x, y, w, h)
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, c, shape_surf.get_rect())
    screen.blit(shape_surf, rect)


AIR_BLOCK = 0
WATER_BLOCK = 1
FULL_PIPE_BLOCK = 2
CARROT_BLOCK  = 3
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
COW_BLOCK = 16
FERTILIZER_BLOCK = 17
VAULT_BLOCK  = 18
MONEY_BLOCK = 19
TRADER_BLOCK = 20

labels = {
    AIR_BLOCK: "air",
    WATER_BLOCK: "water",
    FULL_PIPE_BLOCK: "full pipe",
    CARROT_BLOCK : "carrot",
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
    COW_BLOCK: "cow",
    FERTILIZER_BLOCK: "fertilizer",
    VAULT_BLOCK : "vault wall",
    MONEY_BLOCK: "money",
    TRADER_BLOCK: "trader",
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
    COW_BLOCK: (255, 255, 255),
    FERTILIZER_BLOCK: (0, 80, 0),
    VAULT_BLOCK: (50, 50, 50),
    MONEY_BLOCK: (255, 200, 0),
    TRADER_BLOCK: (0, 255, 0),
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
    11: COW_BLOCK,
    12: FERTILIZER_BLOCK,
    13: VAULT_BLOCK,
    14: TRADER_BLOCK,
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
    TRAPPER_BLOCK: 6,
    AMMO_BLOCK: 1,
    PIPE_BLOCK: 8,
    FULL_PIPE_BLOCK: 8,
    COW_BLOCK: 20,
    FERTILIZER_BLOCK: 2,
    VAULT_BLOCK: 50,
    MONEY_BLOCK: 5,
    TRADER_BLOCK: 20,
}

strength = {
    WALL_BLOCK: 0.94,
    SELLER_BLOCK: 0.5,
    BUYER_BLOCK: 0.7,
    INSERTER1_BLOCK: 0.7,
    INSERTER2_BLOCK: 0.7,
    INSERTER3_BLOCK: 0.7,
    TURRET_BLOCK: 0.85,
    TRAPPER_BLOCK: 0.8,
    AMMO_BLOCK: 0.4,
    PIPE_BLOCK: 0.6,
    FULL_PIPE_BLOCK: 0.6,
    COW_BLOCK: 0.5,
    FERTILIZER_BLOCK: 0,
    VAULT_BLOCK: 0.995,
    MONEY_BLOCK: 0.5,
    TRADER_BLOCK: 0.5,
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

time1 = -20

money = 40000

hardness = 0.99999

selection_held = False

loss = 0

###############################################################################
# Initialize block array
###############################################################################
# sized length x width with each item containing:
# - x location
# - y location
# - block type
# - rabbit priority value
data = np.zeros((length, width, 4), dtype=int)


for i in range(length):
    blocks.append([])
    for j in range(width):
        if area[j][i] > m - 20:
            blocks[i].append([i, j, AIR_BLOCK, 10000])
        else:
            blocks[i].append([i, j, WATER_BLOCK, 10000])


def abs2(value):
    if value < 0:
        value = 0
    return value


# level = int(input("hardness: 1 - 10: "))
level = 5

level = abs2(level - 1) + 1

if level > 10:
    level = 10

level = 11 - level


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

    for j in blocks:
        for i in j:
            if mouse_held[0]:
                if (
                    int(mx / BLOCK_SIZE) == i[0]
                    and int(my / BLOCK_SIZE) == i[1]
                    and i[2] == AIR_BLOCK
                ):
                    if money >= cost[selection[select]]:
                        money -= cost[selection[select]]
                        i[2] = selection[select]
                if (
                    int(mx / BLOCK_SIZE) == i[0]
                    and int(my / BLOCK_SIZE) == i[1]
                    and i[2] in cost
                    and time1 % 12 == 0
                ):
                    if i[2] != selection[select]:
                        money += int(cost[i[2]] / 2)
                        if money >= cost[selection[select]]:
                            money -= cost[selection[select]]
                            i[2] = selection[select]
            if i[2] in cost:
                if mouse_held[2] and time1 % 12 == 0:
                    if int(mx / BLOCK_SIZE) == i[0] and int(my / BLOCK_SIZE) == i[1]:
                        money += int(cost[i[2]] / 2)
                        i[2] = AIR_BLOCK
            if i[2] == WATER_BLOCK:
                if mouse_held[2] and time1 % 12 == 0:
                    if int(mx / BLOCK_SIZE) == i[0] and int(my / BLOCK_SIZE) == i[1]:
                        if money >= 40:
                            i[2] = AIR_BLOCK
                            money -= 40
            if keys[pygame.K_q]:
                try:
                    if int(mx / BLOCK_SIZE) == i[0] and int(my / BLOCK_SIZE) == i[1]:
                        mydic = {}
                        for m in selection.keys():
                            mydic.update({selection[m]: m})
                        select = mydic[i[2]]
                except:
                    pass

    for j in blocks:
        for i in j:
            if i[0] == 0 or i[0] == 58 or i[1] == 0 or i[1] == 28:
                if random.random() > hardness:
                    if i[2] != WATER_BLOCK:
                        i[2] = RABBIT_BLOCK

            if i[2] == AIR_BLOCK:
                continue

            if i[2] == CARROT_BLOCK:
                try:
                    if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                        if random.random() > 0.9995:
                            blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                    if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                        if random.random() > 0.9995:
                            blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                    if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                        if random.random() > 0.9995:
                            blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                    if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                        if random.random() > 0.9995:
                            blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
                except:
                    pass
            elif i[2] == RABBIT_BLOCK and random.random() > 0.9:
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
                    elif u[2] == CARROT_BLOCK or u[2] == COW_BLOCK:
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
                    if random.random() > 0.7:
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
                    if random.random() > 0.7:
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
                    if random.random() > 0.7:
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

                    if u and random.random() > 0.975:
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
                if random.random() > 0.75:
                    i[2] = AIR_BLOCK
            elif i[2] == TRAPPER_BLOCK:
                try:
                    if random.random() > 0.93:
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
                    u = random.choice(s)
                    if u[2] == FULL_PIPE_BLOCK and random.random():
                        i[2] = FULL_PIPE_BLOCK
                        blocks[u[0]][u[1]][2] = PIPE_BLOCK
                    if u[2] == WATER_BLOCK and random.random() > 0.95:
                        i[2] = FULL_PIPE_BLOCK
                except:
                    pass
            elif i[2] == COW_BLOCK and random.random() > 0.96:
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
                            blocks[u[0]][u[1]][2] = COW_BLOCK
                        else:
                            i[2] = COW_BLOCK
                            blocks[u[0]][u[1]][2] = COW_BLOCK

                except:
                    pass
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
                            if random.random() > 0.9985:
                                blocks[o[0]][o[1]][2] = PIPE_BLOCK
                            if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                            if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                            if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                            if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
                        if o[2] == FERTILIZER_BLOCK:
                            if random.random() > 0.9993:
                                blocks[o[0]][o[1]][2] = AIR_BLOCK
                            if blocks[i[0] - 1][i[1]][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0] - 1][i[1]][2] = CARROT_BLOCK
                            if blocks[i[0] + 1][i[1]][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0] + 1][i[1]][2] = CARROT_BLOCK
                            if blocks[i[0]][i[1] - 1][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] - 1][2] = CARROT_BLOCK
                            if blocks[i[0]][i[1] + 1][2] == AIR_BLOCK:
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] + 1][2] = CARROT_BLOCK
            except:
                pass

    if updaterabbitmap:
        for j in blocks:
            for i in j:
                if i[2] in cost:
                    i[3] = 0
                if i[2] == AIR_BLOCK:
                    s = []
                    try:
                        s.append(blocks[i[0]][i[1] + 1])
                    except:
                        pass
                    try:
                        s.append(blocks[i[0]][i[1] - 1])
                    except:
                        pass
                    try:
                        s.append(blocks[i[0] + 1][i[1]])
                    except:
                        pass
                    try:
                        s.append(blocks[i[0] - 1][i[1]])
                    except:
                        pass
                    m = 100
                    for u in s:
                        if u[3] <= m:
                            m = u[3]
                    if not m == 100:
                        i[3] = m + 1

    for j in blocks:
        for i in j:
            # try:
                # image_file = os.path.join(IMAGE_PATH, labels[i[2]] + ".png")
                # image = pygame.image.load(image_file).convert()
                # image.set_colorkey((0, 0, 0))
                # image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))

            image = images[i[2]]
            if image:
                rect = image.get_rect()
                rect.center = (
                    i[0] * BLOCK_SIZE + BLOCK_SIZE / 2,
                    i[1] * BLOCK_SIZE + BLOCK_SIZE / 2,
                )
                screen.blit(image, rect)
            else:
                map1 = pygame.Rect(
                    i[0] * BLOCK_SIZE, i[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(screen, colors[i[2]], map1)
                # add_line(screen, str(i[3]), i[0]*BLOCK_SIZE, i[1]*BLOCK_SIZE)

    rect_alpha(
        int(mx / BLOCK_SIZE) * BLOCK_SIZE,
        int(my / BLOCK_SIZE) * BLOCK_SIZE,
        BLOCK_SIZE,
        BLOCK_SIZE,
        (
            colors[selection[select]][0],
            colors[selection[select]][1],
            colors[selection[select]][2],
            128,
        ),
    )

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
