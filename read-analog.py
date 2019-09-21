import asyncio
import sys
from pymata_express.pymata_express import PymataExpress

# Setup a pin for analog input and monitor its changes


async def the_callback(data):
    """
    A callback function to report data changes.
    :param data: [pin, current reported value, pin_mode, timestamp]
    """
    print(f"analog callback data: {data[1]}  ", end='\r')


async def analog_in(my_board, pin):
    """
    This function establishes the pin as an
    analog input. Any changes on this pin will
    be reported through the call back function.
    Also, the differential parameter is being used.
    The callback will only be called when there is
    difference of 5 or more between the current and
    last value reported.
    :param my_board: a pymata_express instance
    :param pin: Arduino pin number
    """
    await my_board.set_pin_mode_analog_input(pin,
                                             callback=the_callback,
                                             differential=5)
    # run forever waiting for input changes
    while True:
        await asyncio.sleep(1)

# get the event loop
loop = asyncio.get_event_loop()

# instantiate pymata_express
board = PymataExpress()

try:
    # start the main function
    loop.run_until_complete(analog_in(board, 0))
except (KeyboardInterrupt, RuntimeError):
    loop.run_until_complete(board.shutdown())
    sys.exit(0)
