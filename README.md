# x708v2

Forked from https://github.com/geekworm-com/x708v2

## Hardware

* Raspberry Pi 4 8GB
* Geekworm x728-C1 case
* Geekworm x708 hat
* Geekworm x708 UPS

## Software

### bat.py

Monitor battery capacity and voltage. The `Raspberrypi` is turned off if the battery is less than 20%
charged or the capacity is less than 3.0V.

`bat_test.py` can be used to test `bat.py`.

Use `create-bat.service.sh` to create the service to start the `bat.py` script after reboot.

### fan.py

Monitor the `Raspberrypi` temperature is less than minimum threashold or greater that maximum threashold.
Notice tha `x708` fan board is `on` by default, no chance to power off, and the script only control
the fan speed.

Use `create-fan.service.sh` to create the service to start the `fan.py` script after reboot.

### Case power button

`pwr.sh` is the script for power management via case button.


## References

* [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* [x708](https://wiki.geekworm.com/X708?TheOrder=1)
* [x708 software](https://wiki.geekworm.com/X708-Software)
* [x708 hardware](https://wiki.geekworm.com/X708-Hardware)
