import numpy as np
import pandas as pd
from openai import OpenAI
import time
import json
import re
from rapidfuzz import fuzz, process
from tqdm import tqdm
from .classes.structura import Structura
from .classes.machina import Machina
from .classes.utilitas import Utilitas

#TODO: allow enforcing output types for each column

class Batcher:
    # def __init__(self, model: Machina, structura: Structura):
    #     bd = structura
    #     model = model

    @staticmethod
    def _call_batch(batch, model:Machina, bd: Structura):
        if batch.shape[0] < 1:
            print("An empty batch was passed to the _call_batch method.")
            return None

        # Ensure index is 0-based and add an explicit index column
        orig_batch_low, orig_batch_high = batch.index.min(), batch.index.max()
        batch = batch.reset_index(drop=True)
        batch[bd.auto_created_id_name] = batch.index

        joined_rows = []
        for _, row in batch.iterrows():
            row_items = [f'"{col}": "{row[col]}"' for col in bd.INPUT_COLUMN_NAMES]
            row_str = "{ " + f'"{bd.auto_created_id_name}": "{row[bd.auto_created_id_name]}", ' + ", ".join(row_items) + " }"
            joined_rows.append(row_str)
        joined = f'{{"{bd.OUTPUT_OBJECT_NAME}": [\n  ' + ",\n  ".join(joined_rows) + "\n]}}"

        prompt = bd.PROMPT.replace(bd.INPUT_OBJECT_PLACEHOLDER, joined)

        if bd.verbose:
            print(f"Processing rows {orig_batch_low} to {orig_batch_high}")

        response = model.call(prompt, bd)
        
        if bd.verbose:
            print(f"Obtained response for rows {orig_batch_low} to {orig_batch_high}, beginning parsing")

        if not bd.jsonified:
            batch[bd.full_response_column_name] = response
            return batch


        try:
            output = Utilitas.p_json(response, has_separator=True, separator=bd.json_separator, verbose=bd.verbose, best_effort=bd.best_effort)

            if output is None:
                if bd.verbose:
                    print(f"The JSON parser returned None for rows {orig_batch_low} to {orig_batch_high}.")
                batch.loc[0, bd.full_response_column_name] = response
                batch.drop(columns=[bd.auto_created_id_name], inplace=True)
                return batch
            
            output_by_index = {}

            output = Utilitas.fuzz_get(output, bd.OUTPUT_OBJECT_NAME, list, None)
            if output is None:
                if bd.verbose:
                    print(f"The output object '{bd.OUTPUT_OBJECT_NAME}' was not found in the response for rows {orig_batch_low} to {orig_batch_high}.")
                batch.loc[0, bd.full_response_column_name] = response
                batch.drop(columns=[bd.auto_created_id_name], inplace=True)
                return batch
            
            for item in output:
                theID = Utilitas.fuzz_get(item, bd.auto_created_id_name, str, None)
                if theID is not None:
                    o = {}
                    for jtarget in bd.OUTPUT_JSON_KEYS:
                        o[jtarget] = Utilitas.fuzz_get(item, jtarget, str, None)
                    output_by_index[int(theID)] = o

            for target_col, json_key in zip(bd.OUTPUT_COLUMN_NAMES, bd.OUTPUT_JSON_KEYS):
                batch[target_col] = batch[bd.auto_created_id_name].apply(
                    #TODO: set custom default values for each output column
                    lambda idx: output_by_index.get(idx, {}).get(json_key, None)
                )
            # Remove the explicit index column
            batch.loc[0, bd.full_response_column_name] = response #always include the full response - easier to remove after than choose to add
            batch.drop(columns=[bd.auto_created_id_name], inplace=True)
            return batch

        except Exception as e:
            if bd.best_effort:
                print(f"Error in processing rows {orig_batch_low} to {orig_batch_high}: {e}")
                batch[bd.full_response_column_name] = response
                batch.drop(columns=[bd.auto_created_id_name], inplace=True)
                return batch
            else:
                raise e

    @staticmethod
    def call_chunked(df, model: Machina, bd: Structura):
        if df.shape[0] < 1:
            print("An empty batch was passed in. Please confirm this is intentional.")
            return df, 0
        
        if df.shape[0] > 50000:
            cost = model.get_cost_warning(df.shape[0], bd.BATCH_SIZE)
            if cost > 20:
                print(f"Warning - the DataFrame has more than 50,000 rows. While the exact cost is unknown, a rough estimate (using chatgpt 4o model) could be as high as ${cost:.2f}.")
                print("Are you sure you want to continue? (y/n)")
                response = input().strip().lower()
                if response != 'y':
                    print("Batch processing cancelled by user.")
                    return None, 0
                else:
                    print("Continuing with batch processing...")

        # Ensure all columns in batch are added to df, aligning by index
        for col in bd.OUTPUT_COLUMN_NAMES + [bd.full_response_column_name]:
            if col not in df.columns:
                df[col] = ""
        
        start = time.time()
        num_batches = int(np.ceil(df.shape[0] / bd.BATCH_SIZE))


        for i in tqdm(range(num_batches), desc="Processing Batches", unit="batch"):
            start_idx = i * bd.BATCH_SIZE
            end_idx = min((i + 1) * bd.BATCH_SIZE, df.shape[0])
            batch = df.iloc[start_idx:end_idx].copy()

            batch = Batcher._call_batch(batch, model, bd)
            if batch is None and bd.best_effort:
                print(f"Batch {i} processing failed")
                continue
                    
            df.loc[start_idx:end_idx-1, batch.columns] = batch.values


        end = time.time()
        duration = (end - start) * 1000

        return df, duration