import unittest
import time
from hardware.car import Car

class CarTests(unittest.TestCase):
    def setUp(self):
        self.car = Car()

    # Method for returning total distance travelled
    def test_distance_travelled(self):
        self.assertEqual(self.car.get_distance_travelled(), 0,
                        'initial distance is not reported as 0')

    # Method for returning current speed
    def test_get_speed(self):
        self.assertEqual(self.car.get_speed(), 0,
                        'initial speed is not reported as 0')

    # Method for returning acceleratin
    def test_get_acceleration(self):
        self.assertEqual(self.car.get_acceleration(), 0,
                        'initial acceleration is not reported as 0')

    # responds to input - straight
    def test_go_straight(self):
        st = time.time()
        move = self.car.go_straight()
        et = time.time()
        self.assertEqual(move, True, 'go straight command did not work')
        self.assertAlmostEqual(st + 1, et, places=0, 
                        msg='go straight command did not take ~1 sec')

    # responds to input - left
    def test_go_left(self):
        self.assertEqual(self.car.go_left(), True,
                        'go left command did not work')

    # responds to input - left
    def test_go_right(self):
        self.assertEqual(self.car.go_right(), True,
                        'go right command did not work')
    # List all sensors on car
    def test_list_all_sensors(self):
        len_sensors = len(self.car.get_sensors())
        self.assertEqual(len_sensors, 2,
                        'incorrect number of sensors')

    # All sensors are descended from Sensor class
    def test_all_sensors_are_sensors(self):
        sensors = map(get_parent_class, self.car.list_sensors())
        for item in sensors:
            self.assertTrue(item == 'Sensors', 'type of sensor is not Sensor')

    # get_image method returns instance of imagedata class
    def test_get_image(self):
        img = self.car.get_image()
        self.assertEqual(type(img).__name__ == 'ImageData')

    # get_sensor method returns instance of sensordata class
    def test_get_image(self):
        distance = self.car.get_distance()
        self.assertEqual(type(distance).__name__ == 'SensorData')

def get_parent_class(instance_of_class):
    return type(instance_of_class).__bases__[0].__name__