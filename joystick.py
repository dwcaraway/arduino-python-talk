import threading
import asyncio
from pymata_express.pymata_express import PymataExpress
from collections import namedtuple

Bound = namedtuple('Bound', 'lower upper')
JoystickData = namedtuple('JoystickData', 'x y switch')

# Switch digital input
SW_PIN = 2

# X analog input
X_PIN = 0

# Y analog input
Y_PIN = 1

# Changes of +/- this value required to trigger callback, reduces noise
DIFFERENTIAL = 10

# bounds for x value to be considered BACK direction
X_BACK_BOUNDS = Bound(0, 500)

# bounds for x value to be considered FORWARD direction
X_FORWARD_BOUNDS = Bound(540, 1022)

# bounds for y value to be considered DOWN direction
Y_UP_BOUNDS = Bound(0, 500)

# bounds for y value to be considered UP direction
Y_DOWN_BOUNDS = Bound(520, 1022)

# Hold last read pin values in storage. Values are keyed by the pin number.
# TODO need better (threadsafe) storage mechanism
storage = {X_PIN: 0, Y_PIN: 0, SW_PIN: 0}


async def x_handler(data):
    """
    An async callback function to report x input pin changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    val = 0

    if data[1] < X_BACK_BOUNDS.upper:
        val = -1
    elif data[1] > X_FORWARD_BOUNDS.lower:
        val = 1

    storage[data[0]] = val


async def y_handler(data):
    """
    An async callback function to report y input pin changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    val = 0

    # Y axis is inverted, e.g. lower numbers = UP
    if data[1] < Y_UP_BOUNDS.upper:
        val = 1
    elif data[1] > Y_DOWN_BOUNDS.lower:
        val = -1
    storage[data[0]] = val


async def switch_handler(data):
    """
    An async callback function to report switch changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    # the switch goes to 0 when pressed, we flip it so that
    # pressed is 1 and not pressed is 0
    storage[data[0]] = 1 - data[1]


async def print_vals(cb=None):
    """
    Prints storage values to screen.
    Runs until threads do_run is set to false
    : param cb: optional async call back function
    """
    t = threading.current_thread()
    while getattr(t, 'do_run', True):
        if cb:
            jsd = JoystickData(storage[X_PIN], storage[Y_PIN], storage[SW_PIN])
            await cb(jsd)
        else:
            print(f'X-Axis: {storage[X_PIN]}, Y-Axis: {storage[Y_PIN]}, '
                  f'Switch: {storage[SW_PIN]}     ', end='\r')

        await asyncio.sleep(0.05)


def main(event_loop, cb=None):
    """
    Processes the joystick analog and digital inputs
    :param event_loop: the event loop to use for execution
    :param cb: an optional async callback to use
    """
    asyncio.set_event_loop(event_loop)
    board = PymataExpress()

    try:
        pin_setup_task = asyncio.gather(
                board.set_pin_mode_analog_input(X_PIN, callback=x_handler,
                                                differential=DIFFERENTIAL),
                board.set_pin_mode_analog_input(Y_PIN, callback=y_handler,
                                                differential=DIFFERENTIAL),
                board.set_pin_mode_digital_input_pullup(SW_PIN,
                                                        callback=switch_handler)
        )

        event_loop.run_until_complete(pin_setup_task)

        reporting_task = asyncio.ensure_future(print_vals(cb))

        # Now loop forever printing the recorded values
        # from the handlers (callbacks)
        event_loop.run_until_complete(reporting_task)

    except KeyboardInterrupt:
        # hide the keyboard interrupt
        pass
    finally:

        for task in asyncio.Task.all_tasks():
            task.cancel()

        event_loop.run_until_complete(board.shutdown())

        event_loop.stop()


if __name__ == '__main__':
    main(asyncio.get_event_loop())
