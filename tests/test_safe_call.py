import unittest
from CARDUI.safe_call import safe_call

class test_safe_call_runs(unittest.TestCase):

    def test_safe_call(self):
        self.assertEqual(safe_call("hello world"), "hello world")
