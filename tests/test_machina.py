import unittest
from CARDUI import Machina, Structura

class test_machina_runs(unittest.TestCase):

    def test_openai_auth(self):
        machina = Machina(model_provider="OpenAI", model_name="gpt-4o")
        status = machina.auth()
        self.assertEqual(status, "Authentication Success")

    def test_anthropic_auth(self):
        machina = Machina(model_provider="Anthropic", model_name="claude-2")
        status = machina.auth()
        self.assertEqual(status, "Authentication Success")
    
    def test_mistral_auth(self):
        machina = Machina(model_provider="Mistral", model_name="mistral-large")
        status = machina.auth()
        self.assertEqual(status, "Authentication Success")
    
    def test_google_auth(self):
        machina = Machina(model_provider="Google", model_name="gemini-1.5-pro")
        status = machina.auth()
        self.assertEqual(status, "Authentication Success")


    def test_openai_default_chat(self):
        machina = Machina(model_provider="OpenAI", model_name="gpt-4o")
        auth_status = machina.auth()
        response = machina.call("Please say the word 'Hello', and nothing else.")
        self.assertIsNotNone(response)
        self.assertIn("Hello", response)

    def test_anthropic_default_chat(self):
        machina = Machina(model_provider="Anthropic", model_name="claude-3-5-sonnet-latest")
        machina.auth()
        response = machina.call("Please say the word 'Hello', and nothing else.")
        self.assertIsNotNone(response)
        self.assertIn("Hello", response)

    def test_mistral_default_chat(self):
        machina = Machina(model_provider="Mistral", model_name="mistral-large-latest")
        machina.auth()
        response = machina.call("Please say the word 'Hello', and nothing else.")
        self.assertIsNotNone(response)
        self.assertIn("Hello", response)

    def test_google_default_chat(self):
        machina = Machina(model_provider="Google", model_name="gemini-2.5-flash-lite-preview-06-17")
        machina.auth()
        response = machina.call("Please say the word 'Hello', and nothing else.")
        self.assertIsNotNone(response)
        self.assertIn("Hello", response)
