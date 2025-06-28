import re
import json
from rapidfuzz import fuzz

class Utilitas:
    def __init__(self):
        pass

    @staticmethod
    def p_jsonstr(llm_response, separator, **kwargs):

        verbose = kwargs.get("verbose", False)
        best_effort = kwargs.get("best_effort", True)
        errors = ""
        start, end = 0, len(llm_response)
        if start == end:
            errors += "The response is empty. No JSON string could be extracted.\n"
            
        delim_match = list(re.finditer(separator, llm_response))
        if len(delim_match) >= 2:
            start = delim_match[0].end()  
            end = delim_match[-1].start()
        else:
            errors += f"Not enough occurrences of separator '{separator}' in the response.\n"

        #check if "json" prefix was put in:
        if llm_response[start:end].strip().startswith("json"):
            start += 4

        output = llm_response[start:end].strip()
        if not output or len(output) ==0:
            errors += "The extracted JSON string is empty.\n"

        if errors and not best_effort:
            raise ValueError(errors)
        if verbose:
            if errors:
                print(f"⚠️ Warning: {errors.strip()}")
            else:
                print("Parsed the JSON string successfully.")
        return output

    @staticmethod
    def p_float(llm_response, default_value=-1.0, **kwargs):
        verbose = kwargs.get("verbose", False)
        best_effort = kwargs.get("best_effort", True)

        try:
            lint = re.search(r'\d+\.\d+', llm_response)
            return float(lint.group())
        except Exception as e:
            if not best_effort:
                raise ValueError(f"Error in parsing float from response: {e}")
            if verbose:
                print(f"Error in parsing float from response: {e}\n")
            return default_value

    @staticmethod
    def p_int(llm_response, default_value=-1, **kwargs):
        verbose = kwargs.get("verbose", False)
        best_effort = kwargs.get("best_effort", True)
        try:
            lint = re.search(r'\d+', llm_response)
            return int(lint.group())
        except Exception as e:
            if not best_effort:
                raise ValueError(f"Error in parsing integer from response: {e}")
            if verbose:
                print(f"Error in parsing integer from response: {e}\n")
            return default_value

    # @staticmethod
    # def p_json(llm_response, has_separator=True, separator=None):
    #     if has_separator and not separator:
    #         raise ValueError("Separator must be provided if has_separator is True.")
    #     if has_separator:
    #         llm_response = Utilitas.p_jsonstr(llm_response, separator)
    #     try:
    #         lint = json.loads(llm_response)
    #         return lint
    #     except Exception as e:
    #         print(f"Error in parsing JSON from response: {e}")
    #         return None
        

    @staticmethod
    def p_json(llm_response, has_separator=True, separator=None, **kwargs):
        verbose = kwargs.get("verbose", False)
        best_effort = kwargs.get("best_effort", True)
        errors = ""
        try:
            if has_separator and not separator:
                raise ValueError("Separator must be provided if has_separator is True.")
            
            if has_separator:
                llm_response = Utilitas.p_jsonstr(llm_response, separator)

            oout = json.loads(llm_response)
            
            if oout is None and verbose:
                print(f"The JSON parser returned None from input {llm_response!r}. Ensure that your json separator in the structura is correct.")
            return oout
        except json.JSONDecodeError as e:
            errmsg = ""
            errmsg += f"Error when parsing JSON: {e}. The offending portion is marked in red below:\n\n"
            lineno, colno = e.lineno, e.colno
            lines = llm_response.splitlines()
            for i, line in enumerate(lines, 1):
                if i == lineno:
                    prefix = line[:colno-1]
                    highlight = line[colno-1:colno]
                    suffix = line[colno:]
                    errmsg += f"{i:>3}: {prefix}\033[91m{highlight}\033[0m{suffix}\n"  # red error char
                else:
                    errmsg += f"{i:>3}: {line}\n"
            if not best_effort:
                raise ValueError(errmsg)
            if verbose:
                print(f"{errmsg.strip()}")
        except Exception as e:
            if not best_effort:
                raise ValueError(f"Error in parsing JSON from response: {e}")
            if verbose:
                print(f"Unexpected error in parsing JSON from response: {e}\n")
            return llm_response  # Return the raw response if parsing fails

    @staticmethod
    def fuzz_get(obj, search_key, desired_type, default_value=None, **kwargs):
        verbose = kwargs.get("verbose", False)
        best_effort = kwargs.get("best_effort", True)
        errors = ""
        #TODO: implement verbose and best_effort

        score_cuttoff = 80
        if default_value is None:
            default_value = desired_type()

        if not obj:
            return default_value
        
        if not search_key and isinstance(obj, desired_type):
            return obj
        elif not search_key:
            return default_value
        
        if isinstance(obj, dict):
            if search_key in obj and isinstance(obj[search_key], desired_type):
                return obj[search_key]
            else:
                possMatches = []
                for k, v in obj.items():
                    score = fuzz.ratio(search_key, k)
                    if score > score_cuttoff and isinstance(v, desired_type):
                        return v
                    elif score > score_cuttoff:
                        possMatches.append([k, v])
                if len(possMatches) < 1:
                    return default_value
                else:
                    possMatches = sorted(possMatches, key=lambda x: x[1], reverse=True)
                    return possMatches[0][1]
        elif isinstance(obj, desired_type):
            return obj
        else:
            return default_value



        