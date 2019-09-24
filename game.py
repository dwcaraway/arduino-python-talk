import asyncio
import pygame

# Constants
X_MAX = 500  # Max pixels, x-axis
Y_MAX = 500  # Max pixels, y-axis
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 100


class Ball:
    """
    The ball object to manipulate
    """
    def __init__(self):
        self.previous_position = (0, 0)
        self.current_position = (0, 0)
        self.color = BLUE
        self.bg_color = BLACK

    def move(self):
        pass

    def draw(self):
        pass


async def pygame_event_loop(event_queue):
    """
    Gets single event from pygame and loads onto the queue to be processed.
    :param event_queue: the event queue to push events onto
    """
    while True:
        event = pygame.event.wait()
        event_queue.put_nowait(event)


async def handle_events(event_queue):
    while True:
        event = await event_queue.get()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

            if event.key == pygame.K_LEFT:
                new_x = x - vel
                if new_x >= radius - 1:
                    x = new_x
                    update = True

            if event.key == pygame.K_RIGHT:
                new_x = x + vel
                if new_x <= X_MAX - radius:
                    x = new_x
                    update = True

            if event.key == pygame.K_UP:
                new_y = y - vel
                if new_y >= radius - 1:
                    y = new_y
                    update = True

            if event.key == pygame.K_DOWN:
                new_y = y + vel
                if new_y <= Y_MAX - radius:
                    y = new_y
                    update = True

            if event.key == pygame.K_SPACE:
                trailing = not trailing

        else:
            print("unhandled event", event)

    asyncio.get_event_loop().stop()

async def animation(window, ball):
    current_time = 0
    while True:
        last_time, current_time = current_time, time.time()
        await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
# TODO here
        #  ball.move()
        #  screen.fill(black)
        #  ball.draw(screen)
        #  pygame.display.flip()

#  async def otherstuff(window):
    #  # variables
    #  x = 50
    #  y = 50
    #  radius = 20
    #  vel = 10
    #  run = True
    #  trailing = False
#
    #  # draw first circle
#
    #  pygame.draw.circle(window, BLUE, (x, y), radius)
    #  pygame.display.update()
#
    #  run = True
#
    #  while run:
        #  old_x = x
        #  old_y = y
#
        #  update = False
#
        #  pygame.time.delay(100)
#
        #  if update:
            #  if not trailing:
                #  # erase old circle
                #  pygame.draw.circle(window, BLACK, (old_x, old_y), radius)
#
            #  # draw new circle
            #  pygame.draw.circle(window, BLUE, (x, y), radius)
            #  pygame.display.update()


async def main():
    event_queue = asyncio.Queue()

    pygame.init()
    window = pygame.display.set_mode((X_MAX, Y_MAX))
    pygame.display.set_caption("First Game")

    ball = Ball()

    try:
        asyncio.gather(pygame_event_loop(event_queue),
                       otherstuff(window), handle_events(event_queue, ball))
    finally:
        pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())

#  if __name__ == '__main__':
    #  loop = asyncio.get_event_loop()
    #  board = PymataExpress()
#
    #  try:
        #  loop.run_until_complete(main(board))
    #  except KeyboardInterrupt:
        #  # Currently we exit by using CTRL+C, so hide the error
        #  pass
