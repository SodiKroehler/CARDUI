



import unittest
from unittest.mock import patch, MagicMock
from CARDUI import Machina, Structura, Utilitas
from CARDUI import Batcher
import pandas as pd
import sys
import os
import json
import time


class CustomMachina(Machina):
    def __init__(self, model_provider, model_name):
        super().__init__(model_provider, model_name)
        self.client = None  # Custom client initialization if needed

    def auth(self, api_key_env_var=None):
        return "Custom Authentication Success"
    
    def call_full(self, prompt, structura):
        # Simulate a response for testing purposes

        json_sample = {
            "CLEAN": "processed_clean",
            "INPUT2": "processed_input2"
        }
        if structura and structura.jsonified:
            return "```\n" + json.dumps(json_sample) + "\n```"  # Simulate JSON response if jsonified is True
        else:
            return f"Custom response for prompt: {prompt}"


struct1 = Structura()
struct1.PROMPT = "Process the following data: #INPUT_OBJECT_HERE"
struct1.INPUT_COLUMN_NAMES = ["CLEAN", "INPUT2"]
struct1.OUTPUT_JSON_KEYS = ["CLEAN", "INPUT2"]
struct1.jsonify()
struct1.verbose = True
custmod = CustomMachina("CUSTOM", "CUSTOM")
custmod.auth("CUSTOM")

sdf = pd.DataFrame({
    "CLEAN": ["input1", "input2"],
    "INPUT2": ["value3", "value4"]
})

rdf, duration = Batcher.call_chunked(sdf, custmod, struct1)





























# import google.generativeai as genai
# print(genai.__file__)

# # import importlib.util
# # spec = importlib.util.find_spec("google.genai")
# # print(spec)


# import unittest
# from CARDUI import Machina, Structura, Utilitas
# from CARDUI import Batcher
# import pandas as pd

# import sys
# import os
# import json
# sys.path.append(os.path.abspath("./src"))


# class CustomMachina(Machina):
#     def __init__(self, model_provider, model_name):
#         super().__init__(model_provider, model_name)
#         self.client = None  # Custom client initialization if needed

#     def auth(self, api_key_env_var=None):
#         return "Custom Authentication Success"
    
#     def call_full(self, prompt, structura=None):
#         # Simulate a response for testing purposes

#         json_sample = {
#             "clean": "processed_clean",
#             "input2": "processed_input2"
#         }
#         if structura and structura.jsonified:
#             return "```\n" + json.dumps(json_sample) + "\n```"  # Simulate JSON response if jsonified is True
#         else:
#             return f"Custom response for prompt: {prompt}"
    

# # struct1 = Structura()
# # struct1.PROMPT = "Process the following data: #INPUT_OBJECT_HERE"
# # struct1.INPUT_COLUMN_NAMES = ["clean", "input2"]
# # struct1.OUTPUT_JSON_KEYS = ["clean", "input2"]
# # struct1.jsonify()
# custmod = CustomMachina("CUSTOM", "CUSTOM")
# custmod.auth("CUSTOM")

# struct1 = Structura()
# struct1.PROMPT = "Please rate the following customer reviews from 1-10 based on sentiment:\n#MY_INPUT_PLACEHOLDER"
# struct1.INPUT_OBJECT_PLACEHOLDER = "#MY_INPUT_PLACEHOLDER"
# struct1.INPUT_OBJECT_NAME = "reviews"
# struct1.INPUT_COLUMN_NAMES = ["customer_name", "review_body"]
# struct1.INPUT_JSON_KEYS = ["customer", "customer_review"]
# struct1.OUTPUT_OBJECT_NAME = "ratings"
# struct1.OUTPUT_JSON_KEYS = ["score"]
# struct1.OUTPUT_JSON_KEY_DESCRIPTIONS = ["A sentiment score from 1 (very negative) to 10 (very positive)"]
# struct1.OUTPUT_COLUMN_NAMES = ["string_score"]
# struct1.MAX_ANTICIPATED_OUTPUT_LENGTH = 20
# struct1.batch_size = struct1.get_dynamic_batch_size() #sets the max to fit in the context window
# struct1.verbose = True
# struct1.jsonify()  # Enable JSON-based batching and parsing
# print("will convert the prompt to: " + struct1.PROMPT)

# df = pd.DataFrame({
#     "customer_name": ["Alphonzo Dwindli", "Gertrude Maximillian"],
#     "body": ["Gubernatorial Delights found in this ice cream.", "Sasquatach wouldn't eat this ice cream. It's horrible."]
# })

# result_df = Batcher.call_chunked(df, custmod, struct1)

# # # View results
# # <TODO: PUT RESULTS HERE>
# # struct1.verbose = True


# # sdf = pd.DataFrame({
# #     "clean": ["input1", "input2"],
# #     "input2": ["value3", "value4"]
# # })

# # rdf = Batcher._call_batch(sdf, custmod, struct1)
