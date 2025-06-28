# CARDUI 🃏  
**Batch Orchestration Wrapper for LLMs in Python**

cardui is a very simple wrapper over most major LLMS, that also supports within-prompt chunking (sort of like the old openai completions api) for pandas dataframes. It can also be used as just a wrapper for doing LLM processing with dataframes, as it takes less boilerplate and handles rate limiting, context window overflows, ect.

## Installation
```bash
pip install cardui
```
You will have to install either openai, mistralai, google-genai, or anthropic, depending on your model.

Additionally, you will need to obtain an API key, and add it to your environment variables. The auth() method allows passing a non-standard variable name, in case you do not want to use the default name.

Docs for obtaining an API key can be found at:
- [OpenAI / ChatGPT](https://platform.openai.com/account/api-keys)
- [Anthropic / Claude](https://docs.anthropic.com/claude/docs/access-claude-api)
- [Google / Gemini](https://ai.google.dev/gemini-api/docs/api-key)
- [Mistral](https://docs.mistral.ai/getting-started/api-keys/)

---
## ⚡️ Quick Example

```python
from cardui import Machina, Structura, Batcher
import pandas as pd

model = Machina("OpenAI", "gpt-4")  # or "Anthropic", "Mistral", "Google"
struct1 = Structura()
struct1.PROMPT = "Classify the tone of the following sentence as Positive, Negative, or Neutral:\n#INPUT_OBJECT_HERE" 
df = pd.DataFrame({
    "ID": [1, 2],
    "CLEAN": ["This is a long post.", "You are so kind and wonderful!."]
})

result_df, duration = Batcher.call_chunked(df, model, struct1)

```
The results will look like:
| ID | CLEAN                      | LLM_RESPONSE          |
|----|----------------------------|-----------------------|
| 1  | This is a long post.       | Neutral               |
| 2  | This is another.           | Positive              |


---
## Chunked Example
A complete version, with all features explained, is available in all_settings_call.py in the docs folder of the git.

## Feedback or Issues:

Please use the [GitHub Issues](https://github.com/SodiKroehler/CARDUI/issues) tab to:

- Report a bug
- Ask a question
- Request a feature

When submitting a bug, include:
- Steps to reproduce
- Expected vs. actual behavior
- Code snippets or logs if possible
