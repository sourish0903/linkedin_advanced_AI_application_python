from typing import Tuple, Dict
import dotenv
from dotenv import load_dotenv
import os
import requests
import json


EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    load_dotenv()
    EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}'
    response = requests.get(url)
    data = response.json()
    return (base, target, amount, f'{data["conversion_result"]:.2f}')


def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        completion = ...
    except Exception as e:
        print(f"Exception {e} for {text}")
    else:
        return completion

def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")

if __name__ == '__main__':
    print(get_exchange_rate('EUR', 'GBP', '40'))    