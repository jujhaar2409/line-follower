import pygame
import math
import os

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

DARK_GREY = (90, 90, 90)
LIGHT_GREY = (180, 180, 180)

BG_COLOR = LIGHT_GREY
PAINT = DARK_GREY

screen.fill(BG_COLOR)
pygame.display.flip()

mouse = pygame.mouse
canvas = screen.copy()

points = []

THRESHOLD = 0.001
TIME_PER_FRAME = 50


class Car:
    def __init__(self, surface):
        self.direction = pygame.Vector2(1, 0)  # direction of car
        self.is_set = False  # is the car set to the initial position(based on path drawn)
        self.pos = pygame.math.Vector2(100, 400)  # position of the center of the car
        self.theta = 0  # angle of the car with positive x
        self.surface = surface  # surface on which car is drawn
        self.speed = 1.5  # speed of the car
        self.img_original = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'car.png')),
                                                   (100, 100))  # the original image of the car
        self.img = self.img_original  # the current image to be drawn

    def draw(self):
        if len(points) > 1:
            self.step()
        self.surface.blit(self.img, self.pos - pygame.Vector2(self.img.get_size()) / 2)

    def step(self):
        self.pos += self.direction * self.speed

    def turn(self, theta):
        self.theta += theta
        self.direction = pygame.Vector2(math.cos(self.theta), math.sin(self.theta))
        self.img = pygame.transform.rotate(self.img_original, - 180 * self.theta / math.pi)
        self.img = self.img.convert_alpha()

    def set_car(self):
        if len(points) < 10 or car.is_set:
            return
        self.pos = pygame.Vector2(list(points[0]))
        for i, point in enumerate(points):
            if (point - points[0]).magnitude() != 0:
                self.direction = point - points[0]
                self.direction /= self.direction.magnitude()
                self.turn(math.atan2(self.direction.y, self.direction.x))
                self.is_set = True
                return


prev_x = None
prev_y = None


# ignore this function: Helps in drawing the path
def draw_path(brushSize=20, steps=200):
    global prev_x
    global prev_y

    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, PAINT, (x, y), brushSize)

    click = pygame.mouse.get_pressed(3)
    if click[0] == 1:
        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
            pygame.draw.circle(canvas, PAINT, (x, y), brushSize)

        if prev_x is not None:
            diff_x = x - prev_x
            diff_y = y - prev_y
            steps = max(abs(diff_x), abs(diff_y), steps)
            if steps > 0:
                dx = diff_x / steps
                dy = diff_y / steps
                for _ in range(steps):
                    prev_x += dx
                    prev_y += dy
                    pygame.draw.circle(canvas, PAINT, (round(prev_x), round(prev_y)), brushSize)
                    points.append(pygame.math.Vector2(prev_x, prev_y))
        prev_x = x
        prev_y = y
    else:
        prev_x = None
        prev_y = None


clock = pygame.time.Clock()
loop = True
car = Car(screen)
while loop:
    clock.tick(TIME_PER_FRAME)
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed(3)

    screen.fill(BG_COLOR)
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    draw_path(brushSize=30)
    car.draw()

    if not car.is_set and len(points) > 1:
        car.set_car()
    pygame.display.flip()

pygame.quit()
