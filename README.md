# Sense Hat Service UI

## What

Powered by a simple ini file and set as a service to run on boot, Sense Hat Service UI allows you to turn on and off the services you've configured without having to login to the Pi via SSh or VNC. The menu is controlled completely via the joystick and LEDs on the Raspberry Pi Sense Hat. Just add 5V!

## Why

I had a spare Raspberry Pi. 

I thought it would be cool to set up a little computer I could carry with me that would have a variety of services on it. The services would range from development to network security, but I realized that if the services required my to VNC or SSH in first and turn them on manually every time, it would be very helpful (and leaving them all on all the time isn't secure). 

I also had a spare Sense Hat from a previously aboandoned project.

Wouldn't it be cool if you used the joystick on the Sense Hat to manipulate a simple graphical menu on the Sense Hat LED array?

Yes!

This is that.

## How

### Run

Just create a config file, there's a demo ini file included, and run the script like this...

```
./sensehat-ux.py -c services-demo.ini
```

### Installation

Once you have a config ini file, you can install the app as a system service by running 
```
sudo ./install.sh <path to your services.ini>
```

### Uninstallation

Just run the install script again, but with the `--uninstall` flag.
```
sudo ./install.sh --uninstall
```

## Who

This terribly un-idiomatic Python (the Sense Hat API is in Python) has been hacked together by Mike Flynn.
You can find him here: @thatmikeflynn or here: thatmikeflynn.com
