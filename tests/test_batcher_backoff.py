

import unittest
from unittest.mock import patch, MagicMock
from CARDUI import Machina, Structura, Utilitas
from CARDUI import Batcher
import pandas as pd
import sys
import os
import json
import time
from io import StringIO
from openai import RateLimitError
# from anthropic import RateLimitError as anthropic_RateLimitError
# from google.api_core.exceptions import ResourceExhausted
# from mistralai.exceptions import MistralRateLimitException


class test_batcher_withbackoff_runs(unittest.TestCase):
    @patch("time.sleep", return_value=None)  # avoid actual sleep delay
    def test_call_retries_and_warns(self, mock_sleep):
        # Redirect stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        class MockMachina(Machina):
            def __init__(self):
                super().__init__(model_provider="OpenAI", model_name="gpt-4o")
                self.client = MagicMock()
                self.max_retries = 5
                self.warn_retries = 2  # start warning on third failure (i.e., after 2 retries)
                self.backoff_factor = 2
                self.errors_encountered = 0

            def call_full(self, prompt, structura=None):
                raise RateLimitError("Simulated rate limit exceeded")

        model = MockMachina()

        with self.assertRaises(Exception) as cm:
            model.call("test prompt")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        warning_count = output.count("Warning:")
        self.assertEqual(warning_count, 3)
        self.assertIn("Failed to get a response after", str(cm.exception))

        self.assertEqual(mock_sleep.call_count, 5)
        self.assertEqual(model.errors_encountered, 5)
