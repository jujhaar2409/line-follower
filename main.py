import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Line Follower")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)

DARK_GREY = (190, 190, 190)
LIGHT_GREY = (212, 212, 212)

BG_COLOR = DARK_GREY
PAINT = LIGHT_GREY

screen.fill(BG_COLOR)
pygame.display.flip()

mouse = pygame.mouse
fpsClock = pygame.time.Clock()

canvas = screen.copy()

INITIAL_POINT = pygame.math.Vector2((50, 50))
points = [INITIAL_POINT]
# i = 0

prev_x = None # at start there is no previous point
prev_y = None # at start there is no previous point
def airbrush(brushSize = 20):
    global prev_x
    global prev_y

    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, PAINT, (x, y), brushSize)

    click = pygame.mouse.get_pressed(3)
    if click[0] == 1:
        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
            pygame.draw.circle(canvas, PAINT, (x, y), brushSize)
            # points.append(pygame.math.Vector2(x, y))

        # if there is previous point then draw missing points
        if prev_x is not None:
            diff_x = x - prev_x
            diff_y = y - prev_y
            steps = max(abs(diff_x), abs(diff_y)) // 6

            # skip if distance is zero (error: dividing by zero)
            if steps > 0:
                dx = diff_x / steps
                dy = diff_y / steps
                for _ in range(steps):
                    prev_x += dx
                    prev_y += dy
                    pygame.draw.circle(canvas, PAINT, (round(prev_x), round(prev_y)), brushSize)
                    points.append(pygame.math.Vector2(prev_x, prev_y))
        prev_x = x # remeber previous point
        prev_y = y # remeber previous point
    else:
        prev_x = None # there is no previous point
        prev_y = None # there is no previous point

def get_closest_point(mouse_vector):
    min_dist = points[0].distance_to(mouse_vector)
    min_index = -1
    for j, point in enumerate(points):
        dist = points[j].distance_to(mouse_vector)
        if dist < min_dist:
            min_dist = dist
            min_index = j
    return min_dist, min_index

def get_perp():
    mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
    dist, index = get_closest_point(mouse_vector)
    print(dist)
    pygame.draw.line(screen, BLACK, mouse_vector, points[index])
    perp = mouse_vector - points[index]

loop = True
while loop:
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed(3)

    screen.fill(BG_COLOR)
    screen.blit(canvas, (0, 0))
    airbrush()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        get_perp()
    pygame.display.update()

pygame.quit()
