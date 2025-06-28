
from ..static import STANDARD_JSONIFY_PROMPT
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
        
       
        json_prompt = STANDARD_JSONIFY_PROMPT.replace("#OUTPUT_OBJECT_NAME", self.OUTPUT_OBJECT_NAME)
        json_prompt = json_prompt.replace("#auto_created_id_name", self.auto_created_id_name)
        outs = [f"\"{key}\": \"{descr}\"" for key, descr in zip(self.OUTPUT_JSON_KEYS, self.OUTPUT_JSON_KEY_DESCRIPTIONS)]
        json_prompt = json_prompt.replace("#rest_of_the_output_fields", ",\n".join(outs))

        self.PROMPT = self.PROMPT + "\n\n" + json_prompt

        if self.verbose:
            print("Prompt has been jsonified. Full prompt is: ")
            print(self.PROMPT)

        self.jsonified = True
