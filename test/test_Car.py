import unittest
from unittest.mock import Mock, MagicMock, seal, patch
import time
from hardware.car import Car
from hardware.camera import Camera


fake_camera_mock = MagicMock()
def stub_fake_camera():
    return fake_camera_mock

class CarTests(unittest.TestCase):
    def setUp(self):
        engine = Mock(revolutions_per_move=2, move_duration=1)
        engine.go_straight = MagicMock(return_value=True)
        engine.go_left = MagicMock(return_value=True)
        engine.go_right = MagicMock(return_value=True)
        seal(engine.go_straight)
        self.car = Car(engine)

    # Attribute for create time
    def test_created(self):
        self.assertAlmostEqual(self.car.created, time.time(), 1,
                        'object creation date does not match')

    # Camera is defined
    def test_camera(self):
        self.assertIsInstance(self.car.camera, Camera,
                        'camera attribute is not of type Camera')
    
    # Image method returns proper image
    @patch('hardware.camera.Camera.get_latest_image', side_effect=stub_fake_camera)
    def test_get_image(self, mock_cam):
        _ = self.car.get_image()
        self.assertEqual(fake_camera_mock.method_calls[0][0], 'tobase64')

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
