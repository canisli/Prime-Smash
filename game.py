import pygame
import os, sys, argparse
import time
import random
import math
import asyncio

sqrt = math.sqrt
from mathutils import sgn, is_prime, factorize_composite

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test_mode', action='store_true')
    args = parser.parse_args()
    test_mode = args.test_mode

    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps
    max_number = 100

    fruit_colors = (pink:=(222, 66, 121), blue:=(0,0,255), green:=(128,0,0))
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)

    # Length scales in meters
    width = 8
    height = 6
    radius = 0.5
    g = 10
    drag = 'quadratic'
    drag_coeff = 0.5
    pixels_per_meter = 100

    fruits = {}
    counter = 0
    mouse_down = False
    mouse_down_counter = 0
    fail_counter = 0
    score = 0
    high_score = 0

    pygame.init()
    canvas_color = white
    frame = pygame.display.set_mode((width * pixels_per_meter, height*pixels_per_meter))
    frame.fill(canvas_color)
    # font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 32)
    # bigfont = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 40)
    font = pygame.font.SysFont('sans', 32)
    bigfont = pygame.font.SysFont('sans', 40)
    score_text = font.render(str(score), True, black, white)
    pygame.display.update()

    def _generate_fruit(data={}):
        nonlocal counter
        nonlocal mouse_down_counter
        counter += 1
        fruits[counter] = {
            'x' : (x0:=data.get('x',random.uniform(radius, (width - radius)))),
            'y' : data.get('y', height),
            'v_y' : (v_y0:=data.get('v_y', random.uniform(-1.*sqrt(2*g*(height-radius)), -0.9*sqrt(2*g*(height-radius))))),
            'v_x' : data.get('v_x', random.uniform(-(x0-radius)/(-2 * v_y0/g), (width-radius-x0)/(-2 * v_y0/g))),
            'hit' : False,
            'number': (number:=data.get('number', (random.randint(2, max_number)))), 
            'is_prime': is_prime(number),
            'text': bigfont.render(str(number), True, white),
            'color': random.choice(fruit_colors),
            'count': counter,
            'mouse_down_count': mouse_down_counter,
        }
        print(f'{counter}: Created fruit {number} {mouse_down_counter}')

    async def generate_fruits():
        print(f'Generating fruits')
        for i in range(1_000_000_000):
            for j in range(random.randint(1,2)):
                _generate_fruit()

            await asyncio.sleep(4*sqrt(2*height/g))
    
    async def increment_score():
        nonlocal score, high_score
        score += 1
        high_score = max(high_score, score)

    async def fail():
        nonlocal score, high_score, canvas_color, fail_counter
        print(f'fail #{fail_counter}')
        fail_counter += 1
        orig_fail_count = fail_counter
        
        high_score = max(high_score, score)
        score = 0
        canvas_color = (255,canvas_color[1]-40, canvas_color[2]-40) # Get progressively redder

        await asyncio.sleep(0.5)
        if fail_counter == orig_fail_count:
            canvas_color = white

    if test_mode:
        _generate_fruit({'number':21})
    else:
        asyncio.create_task(generate_fruits())

    for i in range(1_000_000_000):
        frame.fill(canvas_color)
        score_text = font.render(str(score), True, black, canvas_color)
        high_score_text = font.render(str(high_score), True, black, canvas_color)
        frame.blit(score_text, (round(width*0.5*pixels_per_meter-20),0))
        frame.blit(high_score_text, (round(width*0.5*pixels_per_meter+20),0))
        for count,fruit in fruits.items():
            fruit['x'] = (fruit['x'] + fruit['v_x'] * dt)
            if fruit['x'] < radius or fruit['x'] > width- radius: # Bounce at walls
                fruit['v_x'] = -1 *fruit['v_x']
            fruit['y'] = fruit['y'] + fruit['v_y'] * dt
            fruit['v_y'] += g * dt
            if drag == 'quadratic':
                fruit['v_y'] -= drag_coeff*fruit['v_y']**2 * sgn(fruit['v_y']) * dt
                fruit['v_x'] -= drag_coeff*fruit['v_x']**2 * sgn(fruit['v_x']) * dt
            elif drag == 'linear':
                fruit['v_y'] -= drag_coeff*fruit['v_y']* dt
                fruit['v_x'] -= drag_coeff*fruit['v_x']* dt


            # Render fruit
            if not fruit['hit'] and fruit['y'] <= height:
                pygame.draw.circle(frame, fruit['color'], center:=(int(fruit['x']*pixels_per_meter), int(fruit['y']*pixels_per_meter)), radius*pixels_per_meter)
                frame.blit(fruit['text'], fruit['text'].get_rect(center=center))

            if not fruit['hit'] and fruit['y'] > height:
                fruit['hit'] = True
                asyncio.create_task(fail())

        # clock.tick(fps)
        await asyncio.sleep(dt)
        # print(clock)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                mouse_down_counter += 1
                print('Mouse down')
                current_position = pygame.mouse.get_pos()
                for count,fruit in fruits.items():
                    if not fruit['hit'] and abs(current_position[0]/pixels_per_meter - fruit['x']) < radius  and abs(current_position[1]/pixels_per_meter - fruit['y']) < radius:
                        # fruit['v_x'] += random.randint(-5, 5)
                        # fruit['v_y'] += random.randint(-5, 5)
                        if fruit['is_prime']:
                            asyncio.create_task(increment_score())
                        else:
                            asyncio.create_task(fail())

                        fruit['hit'] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                print('Mouse up')
                mouse_down = False
            elif mouse_down and event.type == pygame.MOUSEMOTION:
                current_position = pygame.mouse.get_pos()
                for count, fruit in fruits.copy().items():
                    if not fruit['hit'] and mouse_down_counter > fruit['mouse_down_count'] and abs(current_position[0]/pixels_per_meter - fruit['x']) < radius  and abs(current_position[1]/pixels_per_meter - fruit['y']) < radius:
                        fruit['hit'] = True
                        print('SLICE!!!')
                        if fruit['is_prime']:
                            asyncio.create_task(fail())
                        else:
                            asyncio.create_task(increment_score())
                            number = fruit['number']
                            factor = random.choice(list(factorize_composite(number)))

                            v_x1 = random.uniform(0, 3)
                            v_x2 = random.uniform(-3, 0)
                            v_y1 = -8 * fruit['y']/height - abs(random.gauss(0, 1.0))
                            v_y2 =  -8 * fruit['y']/height - abs(random.gauss(0, 1.0))
                            _generate_fruit(data={'number':factor,             'x':fruit['x'], 'y':fruit['y'], 'v_x':v_x1, 'v_y':v_y1})
                            _generate_fruit(data={'number':int(number/factor), 'x':fruit['x'], 'y':fruit['y'], 'v_x':v_x2, 'v_y':v_y2})

                            fruit['v_x'] += random.randint(-5, 5)
                            fruit['v_y'] += random.randint(-5, 5)
                           
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())