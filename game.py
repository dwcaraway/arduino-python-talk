import asyncio
import pygame

pygame.init()

X_MAX = 500
Y_MAX = 500

win = pygame.display.set_mode((X_MAX, Y_MAX))

pygame.display.set_caption("First Game")

CIRCLE_COLOR = (0, 0, 255)  # Blue
BG_COLOR = (0, 0, 0)  # Black

x = 50
y = 50
radius = 20
vel = 10

run = True

pygame.draw.circle(win, CIRCLE_COLOR, (x, y), radius)
pygame.display.update()

while run:
    old_x = x
    old_y = y

    update = False

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        new_x = x - vel
        if new_x >= radius - 1:
            x = new_x
            update = True

    if keys[pygame.K_RIGHT]:
        new_x = x + vel
        if new_x <= X_MAX - radius:
            x = new_x
            update = True

    if keys[pygame.K_UP]:
        new_y = y - vel
        if new_y >= radius - 1:
            y = new_y
            update = True

    if keys[pygame.K_DOWN]:
        new_y = y + vel
        if new_y <= Y_MAX - radius:
            y = new_y
            update = True

    if update:
        # erase old circle
        pygame.draw.circle(win, BG_COLOR, (old_x, old_y), radius)

        # draw new circle
        pygame.draw.circle(win, CIRCLE_COLOR, (x, y), radius)
        pygame.display.update()

pygame.quit()


#  if __name__ == '__main__':
    #  loop = asyncio.get_event_loop()
    #  board = PymataExpress()
#
    #  try:
        #  loop.run_until_complete(main(board))
    #  except KeyboardInterrupt:
        #  # Currently we exit by using CTRL+C, so hide the error
        #  pass
