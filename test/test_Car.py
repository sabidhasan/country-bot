import unittest
from unittest.mock import Mock, MagicMock, seal
import time
from hardware.car import Car

class CarTests(unittest.TestCase):
    def setUp(self):
        engine = Mock(revolutions_per_move=2, move_duration=1)
        engine.go_straight = MagicMock(return_value=True)
        engine.go_left = MagicMock(return_value=True)
        engine.go_right = MagicMock(return_value=True)
        seal(engine.go_straight)
        self.car = Car(engine)

    # Method for returning total distance travelled
    def test_distance_travelled(self):
        self.assertEqual(self.car.get_distance_travelled(), 0,
                        'initial distance is not reported as 0')

    # responds to input - straight
    def test_go_straight(self):
        self.assertEqual(self.car.go_straight(), True,
                        'go straight command did not work')

    # responds to input - left
    def test_go_left(self):
        self.assertEqual(self.car.go_left(), True,
                        'go left command did not work')

    # responds to input - right
    def test_go_right(self):
        self.assertEqual(self.car.go_right(), True,
                        'go right command did not work')
    
    # Method for checking if car is currently moving
    def test_currently_moving(self):
        self.assertEqual(self.car.currently_moving(), False,
                        'car is reported to be moving, when it should not be')

    # Car moves when issued a go_straight command
    def test_currently_moving(self):
        self.car.go_straight()
        self.assertEqual(self.car.currently_moving(), True,
                        'car is reported to be moving, when it should not be')
    
    # When car is made to move, its move counter increases by one
    def test_moves(self):
        self.car.go_left()
        self.assertEqual(self.car.moves, 1, 'car moves are not 1 when moved by 1')
