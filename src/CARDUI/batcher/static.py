#This is not ideal, but is currently the best way I could find. 
# Hoping there is a automatic way in the future!



MODEL_CONTEXT_WINDOW_TOKENS = {
    ("openai", "gpt-4-1106-preview"):       {"input": 128_000, "output": 128_000},
    ("openai", "gpt-4-0125-preview"):       {"input": 128_000, "output": 128_000},
    ("openai", "gpt-4o"):                   {"input": 128_000, "output": 128_000},
    ("openai", "gpt-4"):                    {"input": 32_768,  "output": 32_768},
    ("openai", "gpt-3.5-turbo"):            {"input": 16_385,  "output": 16_385},

    ("anthropic", "claude-4"):              {"input": 1_000_000, "output": 1_000_000},
    ("anthropic", "claude-3-opus"):         {"input": 200_000,  "output": 200_000},
    ("anthropic", "claude-3-sonnet"):       {"input": 200_000,  "output": 200_000},
    ("anthropic", "claude-2.1"):            {"input": 200_000,  "output": 200_000},
    ("anthropic", "claude-2"):              {"input": 100_000,  "output": 100_000},

    ("google", "gemini-pro"):               {"input": 1_000_000, "output": 1_000_000},
    ("google", "gemini-1.5-pro"):           {"input": 1_000_000, "output": 1_000_000},
    ("google", "gemini-2.5-pro"):           {"input": 1_000_000, "output": 1_000_000},
    ("google", "gemini-1-flash"):           {"input": 32_768,   "output": 32_768},

    ("mistral", "mistral-large-2"):         {"input": 128_000,  "output": 128_000},
    ("mistral", "mistral-medium"):          {"input": 32_000,   "output": 32_000},
    ("mistral", "mistral-small"):           {"input": 8_192,    "output": 8_192},

    ("meta", "llama-4-scout"):              {"input": 10_000_000, "output": 10_000_000},  # From Llama 4 Scout news :contentReference[oaicite:1]{index=1}
    ("meta", "llama-4-maverick"):           {"input": 1_000_000, "output": 1_000_000},   # Comparable to GPT‑4o :contentReference[oaicite:2]{index=2}

    # Open‑source / fallback
    ("open_source", "llama-2-7b"):          {"input": 4_096,    "output": 4_096},
    ("open_source", "mixtral-8x7b"):        {"input": 32_000,   "output": 32_000},
}
