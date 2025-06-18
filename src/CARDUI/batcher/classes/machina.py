from .structura import Structura
import os
class Machina:
    def __init__(self, model_provider, model_name):
        self.model_provider = model_provider
        self.model_name = model_name
        self.client = None
    
    def get_default_api_key_name(self):
        if self.model_provider == "OpenAI":
            return "OPENAI_API_KEY"
        elif self.model_provider == "Anthropic":
            return "ANTHROPIC_API_KEY"
        elif self.model_provider == "Mistral":
            return "MISTRAL_API_KEY"
        elif self.model_provider == "Google":
            return "GOOGLE_API_KEY"
        return None

    def auth(self, api_key_env_var=None):
        api_key = None
        if api_key_env_var:
            api_key = os.getenv(api_key_env_var)
        else:
            api_key = os.getenv(self.get_default_api_key_name())

        if not api_key:
            raise ValueError(f"Default API key for {self.model_provider} not found (looking for {self.get_default_api_key_name()}).")
        
        if self.model_provider == "OpenAI":
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)

            try:
                self.client.models.list()
                return "Authentication Success"
            except Exception as e:
                return f"Authentication failed: {e}"

        elif self.model_provider == "Anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)

            try:
                self.client.models.list()
                return "Authentication Success"
            except Exception as e:
                return f"Authentication failed: {e}"
            
        elif self.model_provider == "Mistral":
            from mistralai import Mistral
            self.client = Mistral(api_key=api_key)

            try:
                self.client.models.list()
                return "Authentication Success"
            except Exception as e:
                return f"Authentication failed: {e}"
            
        elif self.model_provider == "Google":
            from google import genai
            self.client = genai.Client(api_key=api_key)

            try:
                self.client.models.list()
                return "Authentication Success"
            except Exception as e:
                return f"Authentication failed: {e}"

    def call_full(self, prompt, structura=None):
        if not self.client:
            raise ValueError("Model client is not authenticated. Call auth() first.")
        
        if structura is None:
            structura = Structura()
    
        if self.model_provider == "OpenAI":
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "developer", "content": structura.system_prompt},
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=structura.temp,
                max_tokens=structura.max_tokens
            )
            return response 
        
        elif self.model_provider == "Anthropic":
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=structura.max_tokens,
                temperature=structura.temp,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system=structura.system_prompt
            )

            return response
        elif self.model_provider == "Mistral":
            response = self.client.chat.complete(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": structura.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=structura.max_tokens,
                temperature=structura.temp
            )
            return response
        elif self.model_provider == "Google":
            from google.genai import types
            # from google.genai.types import GenerationConfig
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=structura.system_prompt,
                    max_output_tokens=structura.max_tokens,
                    temperature=structura.temp,
                ),
                contents=prompt
            )
            return response
        return None
    

    def call(self, prompt):
        response = self.call_full(prompt)
        if self.model_provider == "OpenAI":
            return response.choices[0].message.content
        elif self.model_provider == "Anthropic":
            return response.content[0].text
        elif self.model_provider == "Mistral":
            return response.choices[0].message.content
        elif self.model_provider == "Google":
            return response.text
        
        return None