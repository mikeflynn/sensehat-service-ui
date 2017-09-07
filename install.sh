#!/usr/bin/env bash

SERVICE_NAME="sensehat-ui"

if [ "$1" == "" ]; then
  echo "Missing services.ini path."
  exit 1
fi

if [ "$1" == "--uninstall" ]; then
  # Uninstall logic...
  sudo systemctl stop $SERVICE_NAME
  sudo systemctl disable $SERVICE_NAME
  sudo rm /lib/systemd/system/$SERVICE_NAME.service 
  exit 0
fi

SERVICE_INI="$1"
APP_PATH=$(pwd)

# Generate service file.
SERVICE_FILE=$(cat <<"EOF"
  [Unit]
  Description=Sensehat Service UI
  After=multi-user.target

  [Service]
  Type=simple
  ExecStart=__APP_PATH__/sensehat-ux.py -c __CONFIG_PATH__
  Restart=always
  RestartSec=3

  [Install]
  WantedBy=multi-user.target
EOF
)

SERVICE_FILE="${SERVICE_FILE//__APP_PATH__/$APP_PATH}"
SERVICE_FILE="${SERVICE_FILE//__CONFIG_PATH__/$SERVICE_INI}"

# Stop current service
sudo systemctl stop $SERVICE_NAME.service

# Copy service file to /lib/systemd/system/
sudo echo "$SERVICE_FILE" > /lib/systemd/system/$SERVICE_NAME.service

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME.service
sudo systemctl start $SERVICE_NAME.service

echo "Installation complete."
