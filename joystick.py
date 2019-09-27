import threading
import asyncio
from pymata_express.pymata_express import PymataExpress

# Constants
SW_PIN = 2  # Switch digital output
X_PIN = 0  # X analog output
Y_PIN = 1  # X analog output
CENTER_POINT = 512  # Value of an axis (X or Y) when joystick is centered
DIFFERENTIAL = 10  # Changes of +/- this value required to trigger callback, reduces noise

# Hold last read pin values in storage. Values are keyed by the pin number.
storage = {X_PIN: 0, Y_PIN: 0, SW_PIN: 0}


async def input_handler(data):
    """
    A callback function to report switch changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    val = 0

    if data[0] == X_PIN:
        if data[1] < 500:
            val = -1
        elif data[1] > 540:
            val = 1
        storage[data[0]] = val

    elif data[0] == Y_PIN:
        if data[1] < 500:
            val = 1
        elif data[1] > 520:
            val = -1
        storage[data[0]] = val

    elif data[0] == SW_PIN:
        storage[data[0]] = 1 - data[1]


async def analog_read(board, pin):
    # Use a differential to avoid noise fluctuations on the analog
    await board.set_pin_mode_analog_input(pin, callback=input_handler,
                                          differential=DIFFERENTIAL)

    t = threading.current_thread()
    while getattr(t, 'do_run', True):
        await asyncio.sleep(1)


async def digital_pullup_read(board, pin):
    await board.set_pin_mode_digital_input_pullup(pin, callback=input_handler)

    t = threading.current_thread()
    while getattr(t, 'do_run', True):
        await asyncio.sleep(1)


async def print_vals():
    t = threading.current_thread()
    while getattr(t, 'do_run', True):
        print(f'X-Axis: {storage[X_PIN]}, Y-Axis: {storage[Y_PIN]}, '
              f'Switch: {storage[SW_PIN]}     ', end='\r')
        await asyncio.sleep(0.1)


def main(event_loop=None):
    """
    Processes the joystick analog and digital inputs
    :param event_loop: an optional event loop to use for execution
    """
    asyncio.set_event_loop(event_loop)
    board = PymataExpress()

    try:
        tasks = asyncio.gather(
                analog_read(board, X_PIN),
                analog_read(board, Y_PIN),
                digital_pullup_read(board, SW_PIN),
                print_vals())
        event_loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        tasks.cancel()


if __name__ == '__main__':
    main(loop=asyncio.get_event_loop())
