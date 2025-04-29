import pygame
import random
import os
import math
import time

pygame.init()

BLOCK_SIZE = 28

# Set up the drawing window
screen = pygame.display.set_mode([60*BLOCK_SIZE, 30*BLOCK_SIZE])

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
        freq = 2 ** k
        amp = persistence ** k
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

m *= 1/60/30

for i in range(60):
    blocks.append([])
    for j in range(30):
        if area[j][i] > m - 20:
            blocks[i].append([i, j, 'air', 10000])
        else:
            blocks[i].append([i, j, 'water', 10000])

def rect_alpha(x, y, w, h, c):
    rect = pygame.Rect(x, y, w, h)
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, c, shape_surf.get_rect())
    screen.blit(shape_surf, rect)

colors = {'air': (0, 150, 0), 'carrot': (255, 128, 0), 'wall': (100, 100, 100), 'rabbit': (255, 128, 255), 
          'seller': (255, 200, 0), 'buyer': (128, 100, 0), 'inserter1': (255, 0, 0), 'inserter2': (0, 255, 255), 'inserter3': (0, 255, 128), 
          'turret': (0, 0, 0), 'bullet':(50, 150, 50), 'trapper':(128, 64, 0), 'ammo':(150, 150, 150), 'pipe':(80, 80, 90), 
          'full pipe':(70, 70, 120), 'water':(0, 0, 255), 'cow':(255, 255, 255), 'fertilizer':(0, 80, 0), 
          'vault wall':(50, 50, 50), 'money':(255, 200, 0), 'trader':(0, 255, 0)}

selection = {0: 'carrot', 1: 'wall', 2:'seller', 3:'inserter1', 4:'inserter2', 5:'inserter3', 
             6:'buyer', 7:'turret', 8:'trapper', 9:'ammo', 10:'pipe', 11:'cow', 12:'fertilizer', 13:'vault wall', 14:'trader'}

cost = {'carrot': 4, 'wall': 2, 'seller':20, 'inserter1':4, 'inserter2':4, 'inserter3':4, 
        'buyer':20, 'turret':35, 'bullet':0, 'trapper':6, 'ammo':1, 'pipe':8, 'full pipe':8, 'cow':20, 'fertilizer':2, 'vault wall':50, 'money':5, 'trader':20}

strength = {'wall': 0.94, 'seller':0.5, 'buyer':0.7, 'inserter1':0.7, 'inserter2':0.7, 
            'inserter3':0.7, 'turret':0.85, 'trapper':0.8, 'ammo':0.4, 'pipe':0.6, 'full pipe':0.6, 
            'cow':0.5, 'fertilizer':0, 'vault wall':0.995, 'money':0.5, 'trader':0.5}

select = 0

time1 = -20

money = 40

hardness = 0.99999

selection_held = False

loss = 0

def abs2(value):
    if value < 0:
        value = 0
    return value

level = int(input('hardness: 1 - 10: '))

level = abs2(level - 1) + 1

if level > 10:
    level = 10

level = 11 - level

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
        hardness = 1/(1 - hardness)
        hardness *= 0.99975 + level*0.00002
        hardness = 1 - 1/hardness
    
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
                if int(mx/BLOCK_SIZE) == i[0] and int(my/BLOCK_SIZE) == i[1] and i[2] == 'air':
                    if money >= cost[selection[select]]:
                        money -= cost[selection[select]]
                        i[2] = selection[select]
                if int(mx/BLOCK_SIZE) == i[0] and int(my/BLOCK_SIZE) == i[1] and i[2] in cost and time1 % 12 == 0:
                    if i[2] != selection[select]:
                        money += int(cost[i[2]]/2)
                        if money >= cost[selection[select]]:
                            money -= cost[selection[select]]
                            i[2] = selection[select]
            if i[2] in cost:
                if mouse_held[2] and time1 % 12 == 0:
                    if int(mx/BLOCK_SIZE) == i[0] and int(my/BLOCK_SIZE) == i[1]:
                        money += int(cost[i[2]]/2)
                        i[2] = 'air'
            if i[2] == 'water':
                if mouse_held[2] and time1 % 12 == 0:
                    if int(mx/BLOCK_SIZE) == i[0] and int(my/BLOCK_SIZE) == i[1]:
                        if money >= 40:
                            i[2] = 'air'
                            money -= 40
            if keys[pygame.K_q]:
                try:
                    if int(mx/BLOCK_SIZE) == i[0] and int(my/BLOCK_SIZE) == i[1]:
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
                    if i[2] != 'water':
                        i[2] = 'rabbit'
            
            if i[2] == 'air':
                continue
            
            if i[2] == 'carrot':
                try:
                    if blocks[i[0] - 1][i[1]][2] == 'air':
                        if random.random() > 0.9995:
                            blocks[i[0] - 1][i[1]][2] = 'carrot'
                    if blocks[i[0] + 1][i[1]][2] == 'air':
                        if random.random() > 0.9995:
                            blocks[i[0] + 1][i[1]][2] = 'carrot'
                    if blocks[i[0]][i[1] - 1][2] == 'air':
                        if random.random() > 0.9995:
                            blocks[i[0]][i[1] - 1][2] = 'carrot'
                    if blocks[i[0]][i[1] + 1][2] == 'air':
                        if random.random() > 0.9995:
                            blocks[i[0]][i[1] + 1][2] = 'carrot'
                except:
                    pass
            elif i[2] == 'rabbit' and random.random() > 0.9:
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
                    if u[2] == 'air':
                        i[2] = 'air'
                        blocks[u[0]][u[1]][2] = 'rabbit'
                    elif u[2] == 'carrot' or u[2] == 'cow':
                        loss += int(cost[blocks[u[0]][u[1]][2]]/2)
                        if random.random() < 0.2:
                            blocks[u[0]][u[1]][2] = 'rabbit'
                        else:
                            blocks[u[0]][u[1]][2] = 'air'
                    else:
                        if u[2] in strength:
                            if random.random() > strength[u[2]]:
                                loss += int(cost[blocks[u[0]][u[1]][2]]/2)
                                i[2] = 'air'
                                blocks[u[0]][u[1]][2] = 'rabbit'
                    if random.random() > 0.999:
                        i[2] = 'air'
                except:
                    i[2] = 'air'
            elif i[2] == 'seller':
                try:
                    if blocks[i[0]][i[1] + 1][2] in cost:
                        money += int(cost[blocks[i[0]][i[1] + 1][2]]/2)
                        blocks[i[0]][i[1] + 1][2] = 'air'
                    if blocks[i[0]][i[1] - 1][2] in cost:
                        money += int(cost[blocks[i[0]][i[1] - 1][2]]/2)
                        blocks[i[0]][i[1] - 1][2] = 'air'
                    if blocks[i[0] + 1][i[1]][2] in cost:
                        money += int(cost[blocks[i[0] + 1][i[1]][2]]/2)
                        blocks[i[0] + 1][i[1]][2] = 'air'
                    if blocks[i[0] - 1][i[1]][2] in cost:
                        money += int(cost[blocks[i[0] - 1][i[1]][2]]/2)
                        blocks[i[0] - 1][i[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'trader':
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
                        if b[2] == 'air':
                            if cost[o[2]] >= 5:
                                if random.random() < 5/cost[o[2]]:
                                    blocks[o[0]][o[1]][2] = 'air'
                                blocks[b[0]][b[1]][2] = 'money'
                            else:
                                if random.random() < cost[o[2]]/5:
                                    blocks[b[0]][b[1]][2] = 'money'
                                blocks[o[0]][o[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'inserter1':
                try:
                    if random.random() > 0.7:
                        l = random.choice(['air', 'carrot'])
                        if blocks[i[0]][i[1] + 1][2] in cost and blocks[i[0]][i[1] - 2][2] == l:
                            blocks[i[0]][i[1] - 2][2] = blocks[i[0]][i[1] + 1][2]
                            blocks[i[0]][i[1] + 1][2] = 'air'
                        if blocks[i[0]][i[1] - 1][2] in cost and blocks[i[0]][i[1] + 2][2] == l:
                            blocks[i[0]][i[1] + 2][2] = blocks[i[0]][i[1] - 1][2]
                            blocks[i[0]][i[1] - 1][2] = 'air'
                        if blocks[i[0] + 1][i[1]][2] in cost and blocks[i[0] - 2][i[1]][2] == l:
                            blocks[i[0] - 2][i[1]][2] = blocks[i[0] + 1][i[1]][2]
                            blocks[i[0] + 1][i[1]][2] = 'air'
                        if blocks[i[0] - 1][i[1]][2] in cost and blocks[i[0] + 2][i[1]][2] == l:
                            blocks[i[0] + 2][i[1]][2] = blocks[i[0] - 1][i[1]][2]
                            blocks[i[0] - 1][i[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'inserter2':
                try:
                    if random.random() > 0.7:
                        l = random.choice(['air', 'carrot'])
                        if blocks[i[0]][i[1] - 2][2] in cost and blocks[i[0]][i[1] - 1][2] == l:
                            blocks[i[0]][i[1] - 1][2] = blocks[i[0]][i[1] - 2][2]
                            blocks[i[0]][i[1] - 2][2] = 'air'
                        if blocks[i[0]][i[1] + 2][2] in cost and blocks[i[0]][i[1] + 1][2] == l:
                            blocks[i[0]][i[1] + 1][2] = blocks[i[0]][i[1] + 2][2]
                            blocks[i[0]][i[1] + 2][2] = 'air'
                        if blocks[i[0] - 2][i[1]][2] in cost and blocks[i[0] - 1][i[1]][2] == l:
                            blocks[i[0] - 1][i[1]][2] = blocks[i[0] - 2][i[1]][2]
                            blocks[i[0] - 2][i[1]][2] = 'air'
                        if blocks[i[0] + 2][i[1]][2] in cost and blocks[i[0] + 1][i[1]][2] == l:
                            blocks[i[0] + 1][i[1]][2] = blocks[i[0] + 2][i[1]][2]
                            blocks[i[0] + 2][i[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'inserter3':
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
                            if o[2] == 'air':
                                m.append(o)
                        
                        if m:
                            u = random.choice(m)
                            if blocks[i[0]][i[1] + 2][2] in cost and (u[2] == 'air' or u[2] == 'carrot'):
                                u[2] = blocks[i[0]][i[1] + 2][2]
                                blocks[i[0]][i[1] + 2][2] = 'air'
                            if blocks[i[0]][i[1] - 2][2] in cost and (u[2] == 'air' or u[2] == 'carrot'):
                                u[2] = blocks[i[0]][i[1] - 2][2]
                                blocks[i[0]][i[1] - 2][2] = 'air'
                            if blocks[i[0] + 2][i[1]][2] in cost and (u[2] == 'air' or u[2] == 'carrot'):
                                u[2] = blocks[i[0] + 2][i[1]][2]
                                blocks[i[0] + 2][i[1]][2] = 'air'
                            if blocks[i[0] - 2][i[1]][2] in cost and (u[2] == 'air' or u[2] == 'carrot'):
                                u[2] = blocks[i[0] - 2][i[1]][2]
                                blocks[i[0] - 2][i[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'buyer':
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
                        if b[2] == 'money' and m[2] == 'air':
                            if cost[o[2]] >= 5:
                                if random.random() < 5/cost[o[2]]:
                                    blocks[m[0]][m[1]][2] = o[2]
                                blocks[b[0]][b[1]][2] = 'air'
                            else:
                                if random.random() < cost[o[2]]/5:
                                    blocks[b[0]][b[1]][2] = 'air'
                                blocks[m[0]][m[1]][2] = o[2]
                                
                except:
                    pass
            elif i[2] == 'turret':
                try:
                    s = []
                    s.append(blocks[i[0]][i[1] + 1])
                    s.append(blocks[i[0]][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1]])
                    s.append(blocks[i[0] - 1][i[1]])
                    u = False
                    for o in s:
                        if o[2] == 'ammo':
                            u = True
                    
                    if u and random.random() > 0.975:
                        if blocks[i[0]][i[1] + 1][2] == 'air' or blocks[i[0]][i[1] + 1][2] == 'ammo':
                            blocks[i[0]][i[1] + 1][2] = 'bullet'
                        if blocks[i[0]][i[1] - 1][2] == 'air' or blocks[i[0]][i[1] - 1][2] == 'ammo':
                            blocks[i[0]][i[1] - 1][2] = 'bullet'
                        if blocks[i[0] + 1][i[1]][2] == 'air' or blocks[i[0] + 1][i[1]][2] == 'ammo':
                            blocks[i[0] + 1][i[1]][2] = 'bullet'
                        if blocks[i[0] - 1][i[1]][2] == 'air' or blocks[i[0] - 1][i[1]][2] == 'ammo':
                            blocks[i[0] - 1][i[1]][2] = 'bullet'
                except:
                    pass
            elif i[2] == 'bullet':
                try:
                    s = []
                    s.append(blocks[i[0]][i[1] + 1])
                    s.append(blocks[i[0]][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1]])
                    s.append(blocks[i[0] - 1][i[1]])
                    for u in s:
                        if u[2] == 'rabbit':
                            blocks[u[0]][u[1]][2] = 'air'
                            i[2] = 'air'
                    if i[2] == 'bullet':
                        u = random.choice(s)
                        if u[2] == 'air':
                            i[2] = 'air'
                            blocks[u[0]][u[1]][2] = 'bullet'
                except:
                    i[2] = 'air'
                if random.random() > 0.75:
                    i[2] = 'air'
            elif i[2] == 'trapper':
                try:
                    if random.random() > 0.93:
                        if blocks[i[0]][i[1] + 1][2] == 'rabbit':
                            blocks[i[0]][i[1] + 1][2] = 'air'
                        if blocks[i[0]][i[1] - 1][2] == 'rabbit':
                            blocks[i[0]][i[1] - 1][2] = 'air'
                        if blocks[i[0] + 1][i[1]][2] == 'rabbit':
                            blocks[i[0] + 1][i[1]][2] = 'air'
                        if blocks[i[0] - 1][i[1]][2] == 'rabbit':
                            blocks[i[0] - 1][i[1]][2] = 'air'
                except:
                    pass
            elif i[2] == 'pipe':
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
                    if u[2] == 'full pipe' and random.random():
                        i[2] = 'full pipe'
                        blocks[u[0]][u[1]][2] = 'pipe'
                    if u[2] == 'water' and random.random() > 0.95:
                        i[2] = 'full pipe'
                except:
                    pass
            elif i[2] == 'cow' and random.random() > 0.96:
                try:
                    s = []
                    s.append(blocks[i[0]][i[1] + 1])
                    s.append(blocks[i[0]][i[1] - 1])
                    s.append(blocks[i[0] + 1][i[1]])
                    s.append(blocks[i[0] - 1][i[1]])
                    u = random.choice(s)
                    if u[2] == 'air':
                        if random.random() < 0.9875:
                            i[2] = 'air'
                            blocks[u[0]][u[1]][2] = 'cow'
                        else:
                            i[2] = 'cow'
                            blocks[u[0]][u[1]][2] = 'cow'
                    
                except:
                    pass
            try:
                if i[2] == 'carrot':
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
                        if o[2] == 'full pipe':
                            if random.random() > 0.9985:
                                blocks[o[0]][o[1]][2] = 'pipe'
                            if blocks[i[0] - 1][i[1]][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0] - 1][i[1]][2] = 'carrot'
                            if blocks[i[0] + 1][i[1]][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0] + 1][i[1]][2] = 'carrot'
                            if blocks[i[0]][i[1] - 1][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] - 1][2] = 'carrot'
                            if blocks[i[0]][i[1] + 1][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] + 1][2] = 'carrot'
                        if o[2] == 'fertilizer':
                            if random.random() > 0.9993:
                                blocks[o[0]][o[1]][2] = 'air'
                            if blocks[i[0] - 1][i[1]][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0] - 1][i[1]][2] = 'carrot'
                            if blocks[i[0] + 1][i[1]][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0] + 1][i[1]][2] = 'carrot'
                            if blocks[i[0]][i[1] - 1][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] - 1][2] = 'carrot'
                            if blocks[i[0]][i[1] + 1][2] == 'air':
                                if random.random() > 0.9975:
                                    blocks[i[0]][i[1] + 1][2] = 'carrot'
            except:
                pass
                
    if updaterabbitmap:
        for j in blocks:
            for i in j:
                    if i[2] in cost:
                        i[3] = 0
                    if i[2] == 'air':
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
            try:
                this_dir = os.path.dirname(__file__)
                image_file = os.path.join(this_dir, i[2] + '.png')
                image = pygame.image.load(image_file).convert()
                image.set_colorkey((0, 0, 0))
                image = pygame.transform.scale(image, (BLOCK_SIZE, BLOCK_SIZE))
                rect = image.get_rect()
                rect.center = (i[0]*BLOCK_SIZE + BLOCK_SIZE/2, i[1]*BLOCK_SIZE + BLOCK_SIZE/2)
                screen.blit(image, rect)
            except:
                map1 = pygame.Rect(i[0]*BLOCK_SIZE, i[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, colors[i[2]], map1)
                # add_line(screen, str(i[3]), i[0]*BLOCK_SIZE, i[1]*BLOCK_SIZE)
    
    rect_alpha(int(mx/BLOCK_SIZE)*BLOCK_SIZE, int(my/BLOCK_SIZE)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, 
               (colors[selection[select]][0], colors[selection[select]][1], colors[selection[select]][2], 128))
    
    timer = time.time() - timer
    
    add_line(screen, f'fps: {1/timer :.0f}', 700, 0)
    
    clock = pygame.time.Clock()
    clock.tick(60)
    
    
    add_line(screen, 'selected block: ' + selection[select] + ' cost: ' + str(cost[selection[select]]), 0, 0)
    add_line(screen, 'money: ' + str(int(money)), 0, 30)
    if time1 < 1:
        add_line(screen, f'No rabbits spawning for {-time1/28 :.1f} seconds', 0, 60)
    else:
        add_line(screen, f'rabbit spawning every {1/(1 - (hardness)**180)/7 :.2f} seconds', 0, 60)
    
    add_line(screen, f'loss of money from the rabbits: {loss :.0f}', 0, 90)
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
