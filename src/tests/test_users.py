from Users import User
import unittest
from unittest.mock import patch


class TestUserClass(unittest.TestCase):
    @patch('builtins.input', lambda *args: "testuser1")
    def test_user_instantiation(self):
        testuser = User()
        self.assertEqual(testuser.name, "testuser1", msg="name instantiation error")
