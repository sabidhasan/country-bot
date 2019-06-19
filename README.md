# Run Tests
Run tests by
```
python -m unittest discover
```


# Notes to Self
self.brain for SelfDrivingCar(Car)
Car - acceleration calc'd by distan
      has a moved_timestamps array [] for when move issued
      this allows calculating acceleration and "current speed"
      has a self.car_hardware object that actually talks to hardware