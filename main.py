import pygame
import math

# import os

pygame.init()

WIDTH = 1200
HEIGHT = 800
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
canvas = screen.copy()

# INITIAL_POINT = pygame.math.Vector2((100, 400))
points = []
# points = []

THRESHOLD = 0.001
TIME_PER_FRAME = 50


class Car:
    def __init__(self, surface):
        self.direction = pygame.Vector2(1, 0)
        self.is_set = False
        self.pos = pygame.math.Vector2(100, 400)
        self.theta = 0  # angle with the horizontal
        self.surface = surface
        # self.rect = pygame.Rect(50, 50, 100, 50)
        self.speed = 1.5
        self.radius = 15
        # self.img = pygame.image.load(os.path.join('img', 'car.png'))
        # self.img = pygame.transform.scale(pygame.transform.rotate(self.img, -45), (50, 50))

    def draw(self):
        if len(points) > 1:
            self.step()
        # pygame.draw.rect(self.surface, BLACK, self.rect)
        pygame.draw.circle(self.surface, BLACK, self.pos, self.radius, width=1)
        pygame.draw.line(self.surface, BLACK, self.pos, self.pos + self.direction * 30, 2)
        # pygame.draw.line(self.surface, BLACK, (200, 200), pygame.Vector2(200, 200) + self.direction * 100)
        # self.surface.blit(self.img, self.pos)

    def step(self):
        # self.rect = self.rect.move(self.direction)
        # self.rect.move_ip(self.direction * self.speed)
        self.pos += self.direction * self.speed

    def turn(self, theta):
        self.theta += theta
        self.direction = pygame.Vector2(math.cos(self.theta), math.sin(self.theta))
        # self.img = pygame.transform.rotate(self.img, -180 * theta / math.pi)
        # self.img = pygame.transform.scale(pygame.transform.rotate(self.img, -180 * theta / math.pi), (50, 50))

    def get_angle(self, vec):
        if vec.magnitude() > THRESHOLD:
            # dotprod = math.acos(self.pos.dot(vec) / (vec.magnitude() * self.pos.magnitude()))
            dotprod = math.asin(self.pos.dot(vec) / (vec.magnitude() * self.pos.magnitude()))
            crossprod = self.direction.x * vec.y - self.direction.y * vec.x
            ang = math.copysign(dotprod, crossprod)
            # if crossprod < 0:
            #     ang = dotprod - 90
            # if crossprod > 0:
            #     ang = 270 - dotprod
            return ang
        return 0

    def set_car(self):
        if len(points) < 10 or car.is_set:
            return
        self.pos = pygame.Vector2(list(points[0]))
        for i, point in enumerate(points):
            if (point - points[0]).magnitude() != 0:
                self.direction = point - points[0]
                self.direction /= self.direction.magnitude()
                self.is_set = True
                return


prev_x = None  # at start there is no previous point
prev_y = None  # at start there is no previous point


def airbrush(brushSize=20, steps=200):
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
            steps = max(abs(diff_x), abs(diff_y), steps)

            # skip if distance is zero (error: dividing by zero)
            if steps > 0:
                dx = diff_x / steps
                dy = diff_y / steps
                for _ in range(steps):
                    prev_x += dx
                    prev_y += dy
                    pygame.draw.circle(canvas, PAINT, (round(prev_x), round(prev_y)), brushSize)
                    points.append(pygame.math.Vector2(prev_x, prev_y))
        prev_x = x  # remeber previous point
        prev_y = y  # remeber previous point
    else:
        prev_x = None  # there is no previous point
        prev_y = None  # there is no previous point


def get_closest_point(pos):
    # min_dist = math.inf
    # if len(points) != 0:
    # print(pos)
    # print(len(points))
    min_dist = points[0].distance_to(pos)
    min_index = 0
    for j, point in enumerate(points):
        curr_dist = point.distance_to(pos)
        if curr_dist < min_dist:
            min_dist = curr_dist
            min_index = j
    # print(min_dist)
    return min_dist, min_index


def get_perp(pos):
    # mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
    # dist, index = get_closest_point(mouse_vector)
    the_dist, index = get_closest_point(pos)
    # pygame.draw.line(screen, BLACK, mouse_vector, points[index])
    pygame.draw.line(screen, BLACK, pos, points[index])
    # perp = mouse_vector - points[index]
    the_perp = pos - points[index]
    return the_perp, the_dist


def get_PID_expr(Ki, Kp, Kd, param, prev_param, prev_integral, max_derivative = math.inf):
    derivative = Kd * min((param - prev_param) / TIME_PER_FRAME, max_derivative)
    integral = prev_integral + Ki * (param - prev_param) * TIME_PER_FRAME
    proportion = Kp * param
    # proportion = 0
    ret = - proportion - derivative - integral
    return ret, integral


prev_dist = 0
# prev_angle = 0
dist_integral = 0
# angle_integral = 0


def PID(perp, dist):
    global prev_dist
    # global prev_angle
    global dist_integral
    # global angle_integral

    angle = car.get_angle(perp)
    dist = math.copysign(dist, angle)

    # if abs(angle - math.pi / 2) < math.pi/16:
    #     return -0.02

    max_angle = 0.025
    # weight_a = 0
    weight_d = 1

    dist_PID, dist_integral = get_PID_expr(Kp=0.001, Kd=1, Ki=0, param=dist,prev_integral=dist_integral,  prev_param=prev_dist)
    # angle_PID, angle_integral = get_PID_expr(Kp=0.05, Kd=0.5, Ki=0, param=angle,prev_integral=angle_integral,  prev_param=prev_angle)

    # ret = min(weight_d * dist_PID + weight_a * angle_PID, max_angle)
    ret = min(weight_d * dist_PID, max_angle)

    prev_dist = dist
    # prev_angle = angle
    return ret


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

    airbrush(brushSize=30)
    car.draw()
    if len(points) > 1:
        perp, dist = get_perp(car.pos)
        angle = PID(perp, dist)
        car.turn(angle)
    if not car.is_set and len(points) > 1:
        car.set_car()
    pygame.display.flip()

pygame.quit()
