#!/bin/bash

SERVICE_NAME="/usr/lib/systemd/system/x708-fan.service"

# Create service file on system.
if [ -e $SERVICE_NAME ]; then
        sudo rm $SERVICE_NAME -f
fi

sudo echo '
[Unit]
Description=x708 Fan service

[Service]
ExecStart=/usr/bin/python /home/pi/x708v2/raspberry-pi-os/fan.py
Restart=on-abort
Type=simple

[Install]
WantedBy=multi-user.target
' >> ${SERVICE_NAME}

# create pigpiog service - begin
