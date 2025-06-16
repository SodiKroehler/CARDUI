import unittest
from CARDUI.batcher import call

class test_batcher_runs(unittest.TestCase):

    def test_batcher(self):
        self.assertEqual(call("test batcher"), "test batcher")
