from cardui import Machina, Structura, Batcher
import pandas as pd

#during setup, can override the Machina class to use a custom client, or to mock responses for testing purposes.
# class CustomMachina(Machina):
#     def __init__(self, model_provider, model_name):
#         super().__init__(model_provider, model_name)
#         self.client = None  # Custom client initialization if needed

#     def auth(self, api_key_env_var=None):
#         return "Custom Authentication Success"
    
#     def call_full(self, prompt, structura):
#         # Simulate a response for testing purposes

#         json_sample = {
#             "CLEAN": "processed_clean",
#             "INPUT2": "processed_input2"
#         }
#         if structura and structura.jsonified:
#             return "```\n" + json.dumps(json_sample) + "\n```"  # Simulate JSON response if jsonified is True
#         else:
#             return f"Custom response for prompt: {prompt}"

# machin = CustomMachina("CUSTOM", "CUSTOM")
# machin.auth("CUSTOM")  # Custom authentication, can be any string since it's a mock
# machin.max_retries = 1 

    

machin = Machina("OpenAI", "gpt-4o") #can be most of the main api available models from openai, anthropic, mistral, or google. if a model isn't available that you want - please file a issue for it!
machin.auth() #have to do this before calling a model, will raise an error if the api key isn't set in the environment variables, or if the necessary library isn't installed.
machin.max_retries = 1 #default is 3, turn to 1 to avoid high cost during setup


struc1 = Structura()
#only one placeholder is allowed for now, but any number of input columns can be used. You don't need to prompt to respond in json, that prompt will be added through jsonfify()
struc1.PROMPT = "Please rate the following customer reviews from 1-10 based on sentiment:\n#MY_INPUT_PLACEHOLDER"
struc1.INPUT_OBJECT_PLACEHOLDER = "#MY_INPUT_PLACEHOLDER" #default is #INPUT_OBJECT_HERE, but you can change it to whatever you want.

#see the below prompt for how the below are used
struc1.INPUT_OBJECT_NAME = "reviews" 
struc1.INPUT_COLUMN_NAMES = ["customer_name", "review_body"]
struc1.INPUT_JSON_KEYS = ["customer", "customer_review"]
struc1.OUTPUT_OBJECT_NAME = "ratings"
struc1.OUTPUT_JSON_KEYS = ["score"]
struc1.OUTPUT_JSON_KEY_DESCRIPTIONS = ["A sentiment score from 1 (very negative) to 10 (very positive)"]
struc1.OUTPUT_COLUMN_NAMES = ["string_score"]
struc1.MAX_ANTICIPATED_OUTPUT_WORDS = 201 # only needs to be set if you want to call get_max_batch_size, set to a reasonable max for any 1 response. if a response will respond with multiple values, it should be the longest value
struc1.verbose = True
struc1.jsonify()  # Enable JSON-based batching and parsing

#propmt above turns into this:
'Please rate the following customer reviews from 1-10 based on sentiment:\n#MY_INPUT_PLACEHOLDER\n\n\n        \n        Output your answer in valid JSON, in the following structure:\n\n        ```\n        { \n            ratings: [\n                {\n                    "_ID": "the _ID of the input object",\n                    "score": "A sentiment score from 1 (very negative) to 10 (very positive)"\n                }\n            ]\n        }\n        ```\n        '

df = pd.DataFrame({
    "customer_name": ["Alphonzo Dwindli", "Gertrude Maximillian"],
    "review_body": ["Gubernatorial Delights found in this ice cream.", "Sasquatach wouldn't eat this ice cream. It's horrible."]
})

struc1.batch_size = machin.get_max_batch_size(struc1, df) #optional, sets the max batch size to fit in the context window
#however, default is 1, so it will not batch unless you set it to a higher number.

result_df, duration = Batcher.call_chunked(df, machin, struc1)

#final dataset:
>>> df.head()
          customer_name                                        review_body string_score                                       LLM_RESPONSE
0      Alphonzo Dwindli    Gubernatorial Delights found in this ice cream.            9  ```json\n{ \n    "ratings": [\n        {\n    ...
1  Gertrude Maximillian  Sasquatach wouldn't eat this ice cream. It's h...            1  ```json\n{\n    "ratings": [\n        {\n     ...

