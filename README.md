# Sense Hat Service UI

## What

Powered by a simple ini file and set as a service to run on boot, Sense Hat Service UI allows you to turn on and off the services you've configured without having to login to the Pi via SSh or VNC. The menu is controlled completely via the joystick and LEDs on the Raspberry Pi Sense Hat. Just add 5V!

### Demo

![Start the UI](https://media.giphy.com/media/wLUB4IkG6zVgQ/giphy.gif)

![Use the UI](https://media.giphy.com/media/MInNz1vlXmJnq/giphy.gif)

![Quit the UI](https://media.giphy.com/media/CXpDunwLvJSco/giphy.gif)

## Why

I had a spare Raspberry Pi. 

I thought it would be cool to set up a little computer I could carry with me that would have a variety of services on it. The services would range from development to network security, but I realized that if the services required my to VNC or SSH in first and turn them on manually every time, it would be very helpful (and leaving them all on all the time isn't secure). 

I also had a spare Sense Hat from a previously aboandoned project.

Wouldn't it be cool if you used the joystick on the Sense Hat to manipulate a simple graphical menu on the Sense Hat LED array?

Yes!

This is that.

## How

### Configuration

The services in the menu are all configured with a simple ini file and an example is included in the repo. Each section is an application or service, and each section should have three options: `start`, `stop`, and `status`.

The `start` and `stop` bash commands don't need to return anything other than standard exit, but the `status` command should return a number that is greater than zero if the service is running (`wc -l` works great for this. Ex: `pgrep apache | wc -l`)

```ini
[THING 1]
start: /some/command --start
stop: /some/command --stop
status: pgrep command | wc -l

[THING 2]
start: /some/command --start
stop: /some/command --stop
status: pgrep command | wc -l
```

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

### Reload

If you make changes to the config ini file, you'll need to restart the service to pick up those changes.
```
sudo ./install.sh --reload
```

### Uninstallation

Just run the install script again, but with the `--uninstall` flag.
```
sudo ./install.sh --uninstall
```

## Who

This terribly un-idiomatic Python (the Sense Hat API is in Python) has been hacked together by Mike Flynn.
You can find him here: [@thatmikeflynn](https://twitter.com/thatmikeflynn) or here: [thatmikeflynn.com](http://thatmikeflynn.com) and tell him how Python is awesome and you love that whitespace matters and stuff.
