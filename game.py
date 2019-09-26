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
        self.velocity = 5

    def toggle_trail(self):
        self.trailing = not self.trailing

    def move(self, direction):
        x, y = self.current_position
        update = False

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
            self.previous_positions.append(self.current_position)
            self.current_position = Position(x=x, y=y)

    def draw(self):
        if not self.trailing:
            for position in self.previous_positions:
                pygame.draw.circle(self.window, BLACK, position, self.radius)

        self.previous_positions = []

        pygame.draw.circle(self.window, self.color,
                           self.current_position, self.radius)


def handle_events(ball):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        ball.toggle_trail()

    if keys[pygame.K_LEFT]:
        ball.move(DIR_LEFT)

    if keys[pygame.K_RIGHT]:
        ball.move(DIR_RIGHT)

    if keys[pygame.K_UP]:
        ball.move(DIR_UP)

    if keys[pygame.K_DOWN]:
        ball.move(DIR_DOWN)

    return True


def animation(window, ball):
    running = True

    while running:
        running = handle_events(ball)
        ball.draw()
        pygame.display.update()

        try:
            pygame.time.wait(100)
        except Exception:
            breakpoint()


def main():
    pygame.init()
    pygame.display.set_caption("First Game")
    window = pygame.display.set_mode((X_MAX, Y_MAX))
    ball = Ball(window)

    try:
        animation(window, ball)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()

#  if __name__ == '__main__':
    #  loop = asyncio.get_event_loop()
    #  board = PymataExpress()
#
    #  try:
        #  loop.run_until_complete(main(board))
    #  except KeyboardInterrupt:
        #  # Currently we exit by using CTRL+C, so hide the error
        #  pass
