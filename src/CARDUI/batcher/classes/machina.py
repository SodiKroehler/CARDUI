from .structura import Structura
import os
import time


class Machina:
    def __init__(self, model_provider, model_name):
        self.model_provider = model_provider
        if model_provider not in ["OpenAI", "Anthropic", "Mistral", "Google", "CUSTOM"]:
            raise ValueError("Invalid model provider. Must be one of: OpenAI, Anthropic, Mistral, Google, CUSTOM.")
        self.model_name = model_name
        self.client = None

        if self.model_provider == "CUSTOM":
            self._enforce_overrides(["auth", "call_full"])

        #rate limiting
        self.max_retries = 4
        self.base_delay = 1.0
        self.backoff_factor = 2.0
        self.warn_retries = 2
        self.errors_encountered = 0 #is used in batcher to stop even if best_effort is True

    def _enforce_overrides(self, method_names):
        for method_name in method_names:
            base_method = getattr(Machina, method_name, None)
            sub_method = getattr(self.__class__, method_name, None)
            if base_method is None or sub_method is None:
                raise NotImplementedError(f"Missing required method: {method_name}")
            if sub_method == base_method:
                raise NotImplementedError(
                    f"For CUSTOM provider, you must override `{method_name}()` in your subclass."
                )
    
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

        if not api_key and self.model_provider != "CUSTOM":
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
                    {"role": "developer", "content": structura.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=structura.TEMP,
                max_tokens=structura.MAX_OUTPUT_TOKENS
            )
            return response 
        
        elif self.model_provider == "Anthropic":
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=structura.MAX_OUTPUT_TOKENS,
                temperature=structura.TEMP,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system=structura.SYSTEM_PROMPT
            )

            return response
        elif self.model_provider == "Mistral":
            response = self.client.chat.complete(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": structura.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=structura.MAX_OUTPUT_TOKENS,
                temperature=structura.TEMP
            )
            return response
        elif self.model_provider == "Google":
            from google.genai import types
            # from google.genai.types import GenerationConfig
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=structura.SYSTEM_PROMPT,
                    max_output_tokens=structura.MAX_OUTPUT_TOKENS,
                    temperature=structura.TEMP,
                ),
                contents=prompt
            )
            return response
        return None
    

    def call(self, prompt, structura=None):
        delay = self.base_delay
        retries = 0
        exception = None
        while retries < self.max_retries:
            try:
                response = self.call_full(prompt, structura)
                if self.model_provider == "OpenAI":
                    return response.choices[0].message.content
                elif self.model_provider == "Anthropic":
                    return response.content[0].text
                elif self.model_provider == "Mistral":
                    return response.choices[0].message.content
                elif self.model_provider == "Google":
                    return response.text
                return response
            except Exception as e:
                if retries >= self.warn_retries:
                    print(f"Warning: {e}. Retrying in {delay} seconds...")
                self.errors_encountered += 1
                time.sleep(delay)
                delay *= self.backoff_factor
                retries += 1
                exception = e
        raise Exception(f"Failed to get a response after {self.max_retries} retries. Last error: {exception}")

    def cost_estimate(self, structura, df):
        #very pessimistic estimate and not accurate, but useful for warning
        #TODO_EVENTUALLY: make this more accurate
        tokens_per_row = (structura.MAX_ANTICIPATED_INPUT_WORDS + structura.MAX_ANTICIPATED_OUTPUT_WORDS + len(structura.PROMPT.split())) * 1.3
        total_tokens = df.shape[0] * tokens_per_row
        fouro_price_per_thousand = 0.05
        return total_tokens / 1000 * fouro_price_per_thousand