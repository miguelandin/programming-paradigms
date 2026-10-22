import pygame
from pygame.typing import Point

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

f_range = int(input("rango de la secuencia: "))
secuence: list = [0, 1]

points: list[tuple] = []
for i in range(f_range-1):
    secuence.append(secuence[i]+secuence[i+1])
    points.append((secuence[i], secuence[i+1]))

print(points)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.draw.lines(screen, "red", False, points, 5)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
