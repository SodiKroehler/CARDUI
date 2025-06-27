from ..static import MODEL_CONTEXT_WINDOW_TOKENS
import math as Math

class Structura:

    #TODO: enable mutiple input placeholders?
    #TODO: custom error messages for all error types
    def __init__(self):
        #stuff that's usually set by presets:
        self.SYSTEM_PROMPT = "You are a helpful assistant."
        self.TEMP = 0.1
        self.MAX_OUTPUT_TOKENS = 1000
        self.BATCH_SIZE = 1

        #Stuff that the user always has to set
        self.INPUT_OBJECT_PLACEHOLDER = "#INPUT_OBJECT_HERE" #this has to be in their prompt
        self.INPUT_OBJECT_NAME = "input_object" #what the input json will be called
        self.INPUT_COLUMN_NAMES = ["CLEAN"] #the names of the columns in the input df
        self.INPUT_JSON_KEYS = ["clean"] #the keys in the input json that will be used to fill the columns
        self.OUTPUT_OBJECT_NAME = "generations" #the name of the object that will be returned in the output json
        self.OUTPUT_JSON_KEYS = ["generation"]#the keys in the output json that will be used to fill the columns
        self.OUTPUT_JSON_KEY_DESCRIPTIONS = ["what you think should be here"]#the descriptions of the keys in the output json
        self.OUTPUT_COLUMN_NAMES = [] #the names of the columns in the output df
        self.MAX_ANTICIPATED_OUTPUT_WORDS = -1 #the maximum length of the output in characters, used to calculate the batch size
        self.MAX_ANTICIPATED_INPUT_WORDS = -1 #the maximum length of the input in words, used to calculate the batch size
        self.PROMPT = ""

        #Stuff that should be rarely changed
        self.auto_created_id_name = "_ID" #TODO:what to do if they have a column with this name?
        self.include_full_response = True #can be disabled
        self.full_response_column_name = "LLM_RESPONSE"
        self.json_separator = "```"
        self.max_anticipated_input_length = -1 #if not overridden, will be set to the max length of the input columns
        self.best_effort = True
        self.verbose = False #if True, will print debug information
        
        #private
        self.jsonified = False



    def jsonify(self):
        if self.PROMPT == "":
            raise ValueError("Prompt is not set. Please set the prompt before calling jsonify().")
        
        if self.jsonified:
            return
        
        json_prompt = """
        
        Output your answer in valid JSON, in the following structure:

        ```
        { 
            #OUTPUT_OBJECT_NAME: [
                {
                    "#auto_created_id_name": "the #auto_created_id_name of the input object",
                    #rest_of_the_output_fields
                }
            ]
        }
        ```
        """
        json_prompt = json_prompt.replace("#OUTPUT_OBJECT_NAME", self.OUTPUT_OBJECT_NAME)
        json_prompt = json_prompt.replace("#auto_created_id_name", self.auto_created_id_name)
        outs = [f"\"{key}\": \"{descr}\"" for key, descr in zip(self.OUTPUT_JSON_KEYS, self.OUTPUT_JSON_KEY_DESCRIPTIONS)]
        json_prompt = json_prompt.replace("#rest_of_the_output_fields", ",\n".join(outs))

        self.PROMPT = self.PROMPT + "\n\n" + json_prompt

        if self.verbose:
            print("Prompt has been jsonified. Full prompt is: ")
            print(self.PROMPT)

        self.jsonified = True


    def get_dynamic_batch_size(self, machina):
        if not self.jsonified or self.MAX_ANTICIPATED_OUTPUT_WORDS < 0 or self.MAX_ANTICIPATED_INPUT_WORDS < 0:
            raise ValueError("Cannot get dynamic batch size. Please ensure the prompt is jsonified and MAX_ANTICIPATED_OUTPUT_WORDS and MAX_ANTICIPATED_INPUT_WORDS are set.")
        
        output_overhead = len(self.OUTPUT_JSON_KEYS) * 10
        total_input_tokens = (self.MAX_ANTICIPATED_INPUT_WORDS + len(self.PROMPT.split())) * 1.3 #prompt by now includes overhead
        total_output_tokens = (self.MAX_ANTICIPATED_OUTPUT_WORDS + output_overhead) * 1.3

        # Get the context window size for the current model
        context_window = MODEL_CONTEXT_WINDOW_TOKENS.get((machina.model_provider, machina.model_name), {"input": 0, "output": 0})
        input_tokens = context_window["input"]
        output_tokens = context_window["output"]


        dynamic_batch_size = max(Math.floor(input_tokens / total_input_tokens),
                                     Math.floor(output_tokens / total_output_tokens))

        return dynamic_batch_size