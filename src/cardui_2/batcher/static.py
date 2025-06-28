#This is not ideal, but is currently the best way I could find. 
# Hoping there is a automatic way in the future!


MODEL_CONTEXT_WINDOW_TOKENS = {
     ("openai", "gpt-4-1106-preview"):    128_000,
    ("openai", "gpt-4-0125-preview"):    128_000,
    ("openai", "gpt-4o"):                128_000,
    ("openai", "gpt-4"):                 32_768,
    ("openai", "gpt-3.5-turbo"):         16_385,
    ("openai", "gpt-3.5-turbo-16k"):      16_000,
    ("openai", "gpt-4-turbo"):          128_000,
    ("openai", "gpt-4-32k"):             32_768,
    ("openai", "gpt-4o-mini"):          128_000,
    ("openai", "o1"):                    200_000,
    ("openai", "o1-mini"):               200_000,
    ("openai", "o3"):                    200_000,
    ("openai", "o3-mini"):               200_000,
    ("openai", "o4-mini"):               200_000,
    ("openai", "gpt-4.1"):            1_000_000,
    ("openai", "gpt-4.1-mini"):       1_000_000,
    ("openai", "gpt-4.1-nano"):       1_000_000,

    ("anthropic", "claude-opus-4"):         1_000_000,
    ("anthropic", "claude-sonnet-4"):       1_000_000,
    ("anthropic", "claude-3-7-sonnet"):     200_000,
    ("anthropic", "claude-3-5-sonnet"):     200_000,
    ("anthropic", "claude-3-5-haiku"):      200_000,
    ("anthropic", "claude-3-opus"):         200_000,
    ("anthropic", "claude-3-sonnet"):       200_000,
    ("anthropic", "claude-3-haiku"):        200_000,

    ("google", "gemini-2.5-pro"):         1_000_000,
    ("google", "gemini-2.5-flash"):       1_000_000,
    ("google", "gemini-2.5-flash-lite"):  1_000_000,
    ("google", "gemini-1.5-pro"):           1_000_000,
    ("google", "gemini-1.5-flash"):         32_768,
    ("google", "gemini-2.0-flash"):         1_000_000,
    ("google", "gemini-2.0-flash-thinking"):1_000_000, 
    ("google", "gemini-2.0-pro"):           1_000_000,
    ("google", "gemini-2.0-flash-lite"):     1_000_000,
    ("google", "gemini-1.5-flash-lite"):     1_000_000,

    ("mistral", "mistral-large-2-7b"):   128000,
    ("mistral", "mistral-large-2-13b"):  128000,
    ("mistral", "mistral-large-2-70b"):  128000,
    ("mistral", "mistral-large"):         128000,
    ("mistral", "mistral-large-2"):         128000,
    ("mistral", "mistral-medium"):          32000,
    ("mistral", "mistral-small"):           8192,

    ("meta", "llama-4-scout"):              10000000, 
    ("meta", "llama-4-maverick"):           1000000,
}


STANDARD_JSONIFY_PROMPT = """
        
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