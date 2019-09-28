import asyncio
import pygame
from collections import namedtuple
import threading
from random import randint

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

# Custom pygame event types for joystick
# Joystick pressed up (positive y)
J_UP = pygame.USEREVENT + 1
# Joystick pressed down (negative y)
J_DOWN = pygame.USEREVENT + 2
# Joystick pressed left (negative x)
J_LEFT = pygame.USEREVENT + 3
# Joystick pressed right (positive x)
J_RIGHT = pygame.USEREVENT + 4
# Joystick click down
J_SWITCH = pygame.USEREVENT + 5

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

    def toggle_color(self):
        if self.color == BLUE:
            self.color = Color(randint(0, 255), randint(0, 255), randint(0, 255))
        else:
            self.color = BLUE

    def draw(self):
        if not self.trailing:
            for position in self.previous_positions:
                pygame.draw.circle(self.window, BLACK, position, self.radius)

        self.previous_positions = []

        pygame.draw.circle(self.window, self.color,
                           self.current_position, self.radius)


def handle_events(window, ball):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == J_UP:
            ball.move(DIR_UP)

        if event.type == J_DOWN:
            ball.move(DIR_DOWN)

        if event.type == J_LEFT:
            ball.move(DIR_LEFT)

        if event.type == J_RIGHT:
            ball.move(DIR_RIGHT)

        if event.type == J_SWITCH:
            ball.toggle_color()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        window.fill(BLACK)

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
        running = handle_events(window, ball)
        ball.draw()
        pygame.display.update()

        pygame.time.wait(50)


async def joystick_callback(data):
    """
    Called with joystick X/y/switch value object
    Creates joystick events and adds to the que.

    :param data: a JoystickData
    """
    if data.x > 0:
        ev = pygame.event.Event(J_RIGHT)
        pygame.event.post(ev)
    elif data.x < 0:
        ev = pygame.event.Event(J_LEFT)
        pygame.event.post(ev)

    if data.y > 0:
        ev = pygame.event.Event(J_UP)
        pygame.event.post(ev)
    elif data.y < 0:
        ev = pygame.event.Event(J_DOWN)
        pygame.event.post(ev)

    if data.switch:
        ev = pygame.event.Event(J_SWITCH)
        pygame.event.post(ev)


def main():
    pygame.init()
    pygame.display.set_caption("First Game")
    window = pygame.display.set_mode((X_MAX, Y_MAX))
    ball = Ball(window)

    try:
        import joystick
        # creating thread
        arduino_loop = asyncio.new_event_loop(),
        arduino_thread = threading.Thread(
                target=joystick.main,
                args=(arduino_loop),
                kwargs={'cb': joystick_callback}
        )
        arduino_thread.start()

        animation(window, ball)
    except KeyboardInterrupt:
        pass
    finally:
        arduino_thread.do_run = False
        arduino_thread.join()
        pygame.quit()


if __name__ == '__main__':
    main()
