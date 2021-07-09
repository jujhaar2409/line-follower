import pygame
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Line Follower")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

backgroundImg = pygame.image.load("track.png")

# bot
botImg = pygame.image.load("bot.jpg")
botCurrent = pygame.Vector2()
botCurrent.xy = 146, 320
botEarlier = pygame.Vector2()
botEarlier.xy = 146, 320.2
botVel = pygame.Vector2()  # (velocity) vector along direction of bot
botVelPer = pygame.Vector2()  # perpendicular vector to botVel
botSize = 60  # diameter of bot

# PID
centre = 250
distance = None
errorNew = None
errorEarlier = 0
derivative = 0
integral = 0

# sensors
no_of_sensors = 6
sensorVal = []  # take values 0(black) or 1(white)
sensorCol = []
sensorPosX = []  # position of sensors
sensorPosY = []


def sensorsVal(sensorcol):
    global sensorVal
    for i in range(no_of_sensors):
        rgb = sensorcol[i]
        if rgb[1] > 50 and rgb[2] > 50 and rgb[0] > 50:
            sensorVal.append(1)
        else:
            sensorVal.append(0)


def Distance(sensorVal):
    dist = 500 * sensorVal[5] + 400 * sensorVal[4] + 300 * sensorVal[3] + 200 * sensorVal[2] + 100 * sensorVal[
        1] + 0 * sensorVal[1]
    a = sensorVal[0] + sensorVal[1] + sensorVal[2] + sensorVal[3] + sensorVal[4] + sensorVal[5]
    print(a)
    return dist / a


def PID(errorNew, errorEarlier):
    global derivative, integral
    derivative = errorNew - errorEarlier
    integral += errorNew
    Kp = 0.001
    Kd = 0.0
    Ki = 0.0
    drift_vel = Kp * errorNew + Kd * derivative + Ki * integral
    return drift_vel


running = True
while running:
    screen.fill(black)
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    botVel = botCurrent - botEarlier
    botVelPer = pygame.math.Vector2.rotate(botVel, 90)
    if botVelPer != [0, 0]:
        pygame.math.Vector2.normalize_ip(botVelPer)

    # setting position of sensors
    for i in range(no_of_sensors):
        sensorPosX.append(botCurrent.x + botVelPer.x * (-botSize / 2 + botSize / 5 * i))
        sensorPosY.append(botCurrent.y + botVelPer.y * (-botSize / 2 + botSize / 5 * i))

    # getting the colour under sensors
    for i in range(no_of_sensors):
        sensorCol.append(pygame.Surface.get_at(screen, (int(sensorPosX[i]), int(sensorPosY[i]))))

    sensorsVal(sensorCol)
    distance = Distance(sensorVal)
    errorNew = distance - centre
    drift_Vel = PID(errorNew, errorEarlier)

    screen.blit(botImg, (botCurrent.x-30, botCurrent.y-30))

    botEarlier = botCurrent
    botCurrent = botCurrent + botVel + botVelPer * (-drift_Vel)
    print(botCurrent)
    print(botVel)
    print(botVelPer)
    print(sensorVal)
    sensorVal = []  # take values 0(black) or 1(white)
    sensorCol = []
    sensorPosX = []  # position of sensors
    sensorPosY = []
    errorEarlier = errorNew
    pygame.display.update()
