import pygame
import sys
import math


SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

MAP = (
    '########'
    '# #    #'
    '# #   ##'
    '#      #'
    '#      #'
    '#  ##  #'
    '#   #  #'
    '########'
)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Py-caster")

clock = pygame.time.Clock()


def draw_map():
    for row in range(8):
        for col in range(8):
            sqaure = row * MAP_SIZE + col

            pygame.draw.rect(
                screen, 
                (200, 200, 200) if MAP[sqaure] == '#' else (100, 100, 100),
                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )

    # draw player
    pygame.draw.circle(
        screen, 
        (255, 0, 0), 
        (int(player_x), int(player_y)), 
        8
    )

    # draw player direction
    pygame.draw.line(
        screen, 
        (0, 255, 0), 
        (player_x, player_y), 
        (
            player_x - math.sin(player_angle) * 50, 
            player_y + math.cos(player_angle)* 50
        ), 
        3
    )

    # draw player FOV
    pygame.draw.line(
        screen, 
        (0, 255, 0), 
        (player_x, player_y), 
        (
            player_x - math.sin(player_angle - HALF_FOV) * 50, 
            player_y + math.cos(player_angle - HALF_FOV) * 50
        ), 
        3
    )

    pygame.draw.line(
        screen, 
        (0, 255, 0), 
        (player_x, player_y), 
        (
            player_x - math.sin(player_angle + HALF_FOV) * 50, 
            player_y + math.cos(player_angle + HALF_FOV)* 50
        ), 
        3
    )

# raycasting algorithm
def cast_rays():
    start_angle = player_angle - HALF_FOV

    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth
            
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            square = row * MAP_SIZE + col

            if MAP[square] == '#':
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (
                        col * TILE_SIZE,
                        row * TILE_SIZE,
                        TILE_SIZE - 2,
                        TILE_SIZE -2
                    )
                )

                # draw rays
                pygame.draw.line(
                    screen, 
                    (0, 212, 0), 
                    (player_x, player_y), 
                    (target_x, target_y), 
                    3
                )

                # wall shading
                color = 255 / (1 + depth * depth * 0.0001)
                
                # fix fish eye effect
                depth *= math.cos(player_angle - start_angle)

                # calculate the height
                wall_height = 21000 / (depth + 0.0001)
                
                if wall_height > SCREEN_HEIGHT:
                    wall_height = SCREEN_HEIGHT

                # drawing 3D view
                pygame.draw.rect(screen, (color , color , color), 
                    (
                        SCREEN_HEIGHT + ray * SCALE, 
                        (SCREEN_HEIGHT / 2) - wall_height / 2, 
                        SCALE, 
                        wall_height
                    )
                )

                break

        start_angle += STEP_ANGLE

fowrward = True

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)

    square = row * MAP_SIZE + col

    if MAP[square] == '#':
        if fowrward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    # 2D view
    pygame.draw.rect(
        screen, 
        (0, 0, 0), 
        (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT)
    )

    # 3D view
    # floor
    pygame.draw.rect(
        screen, 
        (100, 100, 100), 
        (480, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    #ceiling
    pygame.draw.rect(
        screen, 
        (200, 200, 200), 
        (480, -SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    draw_map()
    cast_rays()

    keys = pygame.key.get_pressed()
    
    # player movment
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
    if keys[pygame.K_UP]:
        fowrward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        fowrward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5


    clock.tick(30)

    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    fps_surface = font.render(fps, False, (0, 0, 0))
    screen.blit(fps_surface, (480, 0))

    pygame.display.flip()