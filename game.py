import pygame, sys, os
import time
import random
import math
sqrt = math.sqrt

# Length scales in meters
width = 8
height = 6
radius = 0.5
g = 10 
pixels_per_meter = 100

white = (255,255,255)
black = (0,0,0)
clock = pygame.time.Clock()

score = 0

fps = 30
dt = 1/fps

fruits = ['watermelon', 'orange']

pygame.init()
frame = pygame.display.set_mode((width * pixels_per_meter, height*pixels_per_meter))
frame.fill(white)
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 32)
score_text = font.render(str(score), True, black, white)

fruit_colors = (pink:=(222, 66, 121), blue:=(0,0,255), green:=(128,0,0))
white= (255,255,255)
bigfont = pygame.font.SysFont("arial", 40)

def generate_random_fruits(fruit):
    data[fruit] = {
        'x' : (x0:=random.uniform(radius, (width - radius))),
        'y' : height,
        'v_y' : (v_y0:=random.uniform(-sqrt(2*g*(height-radius)), -0.75*sqrt(2*g*(height-radius)))),
        'v_x' : random.uniform(-(x0-radius)/(-2 * v_y0/g), (width-radius-x0)/(-2 * v_y0/g)),
        'throw' : False,
        't' : 0,
        'hit' : False,
        'number': (number:=random.randint(1, 1000)),
        'text': bigfont.render(str(number), True, white),
        'color': random.choice(fruit_colors)
    }

    print(v_y0)

    if(random.random() >= 0.75):
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

pygame.display.update()

while True:
    frame.fill(white)
    frame.blit(score_text, (0,0))
    for key,value in data.items():
        if value['throw']:
            value['x'] = value['x'] + value['v_x'] * dt
            value['y'] = value['y'] + value['v_y'] * dt
            value['v_y'] += g * dt
            value['t'] += dt

            # Render fruit
            if value['y'] <= height:
                pygame.draw.circle(frame, value['color'], center:=(int(value['x']*pixels_per_meter), int(value['y']*pixels_per_meter)), radius*pixels_per_meter)
                frame.blit(value['text'], value['text'].get_rect(center=center))
            else:
                generate_random_fruits(key)
            
            current_position = pygame.mouse.get_pos()
            if not value['hit'] and abs(current_position[0]/pixels_per_meter - value['x']) < radius  and abs(current_position[1]/pixels_per_meter - value['y']) < radius:
                path = os.path.join(os.getcwd(),'half_'+key+'.png')
                value['img'] = pygame.image.load(path)
                # value['v_x'] += random.randint(-5, 5)
                # value['v_y'] += random.randint(-5, 5)
                score += 1
                score_text = font.render(str(score), True, black, white)
                value['hit'] = True

        else:
            generate_random_fruits(key)

    clock.tick(fps)
    # print(clock)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    