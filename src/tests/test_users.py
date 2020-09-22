from Users import User
import unittest
from unittest.mock import patch


class TestUserClass(unittest.TestCase):
    def test_user_instantiation(self):
        @patch('builtins.input', lambda *args: "testuser1")
        testuser = User()
        self.assertEqual(testuser.name, "testuser1", msg="name instantiation error")

        @patch('builtins.input', lambda *args: "Groot")
        testuser = User()
        self.assertEqual(testuser.name, "Groot", msg="name instantiation error")
