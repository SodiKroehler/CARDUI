# CARDUI 🃏  
**Batch Orchestration Wrapper for LLMs in Python**

CARDUI is a very simple wrapper over most major LLMS, that also supports within-prompt chunking (sort of like the old openai completions api) for pandas dataframes. It can also be used as just a wrapper for doing LLM processing with dataframes, as it takes less boilerplate and handles rate limiting, context window overflows, ect.

---
## ⚡️ Quick Example

```python
from CARDUI import Machina, Structura, Batcher
import pandas as pd

# Step 1: Load your model (set relevant API keys in env vars), or supply custom name here
model = Machina("OpenAI", "gpt-4")  # or "Anthropic", "Mistral", "Google"

# Step 2: Define details
struct1 = Structura()
struct1.PROMPT = "Summarize each item below:\n#INPUT_OBJECT_HERE" 

#Note: defaults to replace #INPUT_OBJECT_HERE with the value of each "CLEAN" row

# Step 3: Run it on a DataFrame
df = pd.DataFrame({
    "ID": [1, 2],
    "CLEAN": ["This is a long post.", "This is another."]
})

result_df, duration = Batcher.call_chunked(df, model, struct1)

# View results
<TODO: PUT RESULTS HERE>
```

---
## Chunked Example

```python
from CARDUI import Machina, Structura, Batcher
import pandas as pd

model = Machina("OpenAI", "gpt-4")  # or "Anthropic", "Mistral", "Google"

struct = Structura()
struct.PROMPT = "Please rate the following customer reviews from 1-10 based on sentiment:\n#MY_INPUT_PLACEHOLDER"
struct.INPUT_OBJECT_PLACEHOLDER = "#MY_INPUT_PLACEHOLDER"
struct.INPUT_OBJECT_NAME = "reviews"
struct.INPUT_COLUMN_NAMES = ["customer_name", "review_body"]
struct.INPUT_JSON_KEYS = ["customer", "customer_review"]
struct.OUTPUT_OBJECT_NAME = "ratings"
struct.OUTPUT_JSON_KEYS = ["score"]
struct.OUTPUT_JSON_KEY_DESCRIPTIONS = ["A sentiment score from 1 (very negative) to 10 (very positive)"]
struct.OUTPUT_COLUMN_NAMES = ["string_score"]
struct.MAX_ANTICIPATED_OUTPUT_LENGTH = 20
struct.batch_size = struct.get_dynamic_batch_size() #sets the max to fit in the context window
struct.verbose = True
struct.jsonify()  # Enable JSON-based batching and parsing

df = pd.DataFrame({
    "customer_name": ["Alphonzo Dwindli", "Gertrude Maximillian"],
    "body": ["Gubernatorial Delights found in this ice cream.", "Sasquatach wouldn't eat this ice cream. It's horrible."]
})

result_df, duration = Batcher.call_chunked(df, model, struct)

# View results
<TODO: PUT RESULTS HERE>
```