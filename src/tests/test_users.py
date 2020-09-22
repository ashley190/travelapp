from Users import User
import unittest
from unittest.mock import patch


class TestUserClass(unittest.TestCase):
    @patch('builtins.input', side_effect = ["testuser1", "Groot", "Ares"])
    def test_user_instantiation(self, User):
        testuser1 = User()
        testuser2 = User()
        testuser3 = User()
        self.assertTrue(testuser1 == "testuser1")
        self.assertTrue(testuser2 == "Groot")
        self.assertTrue(testuser3 == "Ares")