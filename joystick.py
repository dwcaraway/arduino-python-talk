import asyncio
from pymata_express.pymata_express import PymataExpress

# Constants
SW_PIN = 2  # Switch digital output
X_PIN = 0  # X analog output
Y_PIN = 1  # X analog output

# Hold last read pin values in storage. Values are keyed by the pin number.
storage = {X_PIN: '512', Y_PIN: '512', SW_PIN: '1'}


async def print_callback(data):
    """
    A callback function to report switch changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    storage[data[0]] = data[1]
    print(f'X-Axis: {storage[X_PIN]}, Y-Axis: {storage[Y_PIN]}, '
          f'Switch: {storage[SW_PIN]}     ', end='\r')


async def analog_read(board, pin):
    # Use a differential to avoid noise fluctuations on the analog
    await board.set_pin_mode_analog_input(pin, callback=print_callback,
                                          differential=3)

    while True:
        await asyncio.sleep(1)


async def digital_pullup_read(board, pin):
    await board.set_pin_mode_digital_input_pullup(pin, callback=print_callback)

    while True:
        await asyncio.sleep(1)


async def main(board):
    """
    Processes the joystick analog and digital inputs
     :param my_board: a pymata_express instance
    """
    await asyncio.gather(
            analog_read(board, X_PIN),
            analog_read(board, Y_PIN),
            digital_pullup_read(board, SW_PIN),
            )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    board = PymataExpress()

    try:
        loop.run_until_complete(main(board))
    except KeyboardInterrupt:
        # Currently we exit by using CTRL+C, so hide the error
        pass
