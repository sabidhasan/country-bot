# Run Tests
Run tests by
```
python -m unittest discover
```
RPi module cannot run on non-RPi devices. To get around this, a dummy fake RPi module is used as a mock.

# Dependencies
Enable camera in raspberry pi settings: `raspbian-config`
- `python3-picamera`
- `opencv-python`
- `BotFakeRPi` (adapted from https://github.com/sn4k3/FakeRPi)


# Notes to Self

self.brain for SelfDrivingCar(Car)
Car - acceleration calc'd by distan
      has a moved_timestamps array [] for when move issued
      this allows calculating acceleration and "current speed"
      has a self.car_hardware object that actually talks to hardware