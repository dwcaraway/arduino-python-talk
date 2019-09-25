import time
import asyncio
import pygame
from collections import namedtuple

Color = namedtuple('Color', 'red green blue')
Position = namedtuple('Position', 'x y')

# Constants
X_MAX = 500  # Max pixels, x-axis
Y_MAX = 500  # Max pixels, y-axis
FPS = 100
BLUE = Color(red=0, green=0, blue=255)
BLACK = Color(red=0, green=0, blue=0)
DIR_UP = 'up'
DIR_DOWN = 'down'
DIR_LEFT = 'left'
DIR_RIGHT = 'right'


class Ball:
    """
    The ball object to manipulate
    """
    def __init__(self, window):
        self.previous_positions = []
        self.current_position = Position(x=50, y=50)
        self.color = BLUE
        self.bg_color = BLACK
        self.radius = 20
        self.window = window
        self.trailing = False
        self.velocity = 1

    def move(self, direction):

        update = False
        x, y = self.current_position

        if direction == DIR_UP:
            y -= self.velocity

            if y >= self.radius - 1:
                update = True

        elif direction == DIR_DOWN:
            y += self.velocity

            if y <= Y_MAX - self.radius:
                update = True

        elif direction == DIR_LEFT:
            x -= self.velocity

            if x >= self.radius-1:
                update = True

        elif direction == DIR_RIGHT:
            x += self.velocity

            if x <= X_MAX - self.radius:
                update = True
        else:
            raise Exception('Invalid direction')

        if update:
            self.previous_positions.push(self.current_position)
            self.current_position = Position(x=x, y=y)

    def draw(self):
        pygame.draw.circle(self.window, self.color,
                           self.current_position, self.radius)

        if not self.trailing:
            for position in self.previous_positions:
                pygame.draw.circle(self.window, BLACK, position, self.radius)

        self.previous_positions = []


async def pygame_event_loop(event_queue):
    """
    Gets single event from pygame and loads onto the queue to be processed.
    :param event_queue: the event queue to push events onto
    """
    while True:
        event = pygame.event.wait()
        event_queue.put_nowait(event)


async def handle_events(event_queue, ball):
    while True:
        event = await event_queue.get()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.trailing = not ball.trailing

            if event.key == pygame.K_LEFT:
                ball.move(DIR_LEFT)

            if event.key == pygame.K_RIGHT:
                ball.move(DIR_RIGHT)

            if event.key == pygame.K_UP:
                ball.move(DIR_UP)

            if event.key == pygame.K_DOWN:
                ball.move(DIR_DOWN)
        else:
            print("unhandled event", event)

    asyncio.get_event_loop().stop()


async def animation(window, ball):
    current_time = 0

    while True:
        last_time, current_time = current_time, time.time()
        await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
        pygame.display.update()


async def main():

    event_queue = asyncio.Queue()
    window = pygame.display.set_mode((X_MAX, Y_MAX))
    pygame.display.set_caption("First Game")

    ball = Ball(window)

    try:
        asyncio.gather(pygame_event_loop(event_queue),
                       handle_events(event_queue, ball),
                       animation(window, ball))
    finally:
        pygame.quit()


if __name__ == '__main__':
    pygame.init()

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
