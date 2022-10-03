#!/usr/bin/env python3

import subprocess
import time
import sys
import logging
import logging.handlers as handlers

from gpiozero import OutputDevice


logger = logging.getLogger("fan")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logHandler = handlers.RotatingFileHandler(
    "/home/pi/x708v2/raspberry-pi-os/x708.log",
    mode="a",
    maxBytes=1000000,
    backupCount=1,
    encoding="utf-8",
    delay=0,
)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


ON_THRESHOLD = 50.0  # (degrees Celsius) Fan running at this temperature.
OFF_THRESHOLD = 40.0  # (degress Celsius) Fan not running at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_FAN = 16  # Do not change pin 16


def get_temp():
    """Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    output = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True)
    temp_str = output.stdout.decode()

    try:
        return float(temp_str.split("=")[1].split("'")[0])
    except (IndexError, ValueError):
        raise RuntimeError("Could not parse temperature output.")


if __name__ == "__main__":
    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError("OFF_THRESHOLD must be less than ON_THRESHOLD")

    fan = OutputDevice(GPIO_FAN)

        # Fan is OFF by default
    fan.off()

    try:
        while True:
            temp = get_temp()
            # On, fan not running and temperature has reached the limit.
            # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
            if not fan.value and temp >= ON_THRESHOLD:
                logger.info("Fan ON")
                fan.on()

            # Off, fan is running and temperature has dropped below the limit.
            elif fan.value and temp <= OFF_THRESHOLD:
                logger.info("Fan OFF")
                fan.off()

            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
        sys.exit(0)
