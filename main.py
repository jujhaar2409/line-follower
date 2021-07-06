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

loop = True
while loop:
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed(3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif left_pressed:
            pygame.draw.circle(canvas, PAINT, (pygame.mouse.get_pos()), 30)

    screen.fill(BG_COLOR)
    screen.blit(canvas, (0, 0))
    # pygame.draw.circle(screen, PAINT, (mouse.get_pos()), 30)
    print(screen.get_at(mouse.get_pos()))

    pygame.display.update()

pygame.quit()
