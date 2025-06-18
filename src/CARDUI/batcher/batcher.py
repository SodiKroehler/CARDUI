import numpy as np
import pandas as pd
from openai import OpenAI
import time
import json
import re
from rapidfuzz import fuzz, process
from tqdm import tqdm


def call(text):
    return text