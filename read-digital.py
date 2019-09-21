import asyncio
import sys
from pymata_express.pymata_express import PymataExpress


# Setup a pin for digital input and monitor its changes
# Both polling and callback are being used in this example.

async def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print(f'Pin {data[0]}: {data[1]}  ', end='\r')


async def digital_in(my_board, pin):
    """
     This function establishes the pin as a
     digital input. Any changes on this pin will
     be reported through the call back function.
     :param my_board: a pymata_express instance
     :param pin: Arduino pin number
     """
    # set the pin mode

    await my_board.set_pin_mode_digital_input_pullup(pin, callback=the_callback)

    while True:
        await my_board.digital_read(pin)

        while True:
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
board = PymataExpress()
try:
    loop.run_until_complete(digital_in(board, 2))
    loop.run_until_complete(board.shutdown())
except KeyboardInterrupt:
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
