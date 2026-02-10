from typing import Tuple, Dict
import dotenv
from dotenv import load_dotenv
import os
import requests
import json
import streamlit as st
import os
from openai import OpenAI

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    load_dotenv()
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}'
    response = requests.get(url)
    data = response.json()
    return (base, target, amount, f'{data["conversion_result"]:.2f}')


def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    functions = [
        {
            "name": "get_exchange_rate",
            "description": "Get current exchange rate value using the function arguments from https://v6.exchangerate-api.com/v6.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base": {
                        "type": "string",
                        "description": "Base currency(e.g. 'GBP'.),the currency the prompt asking to convert. eg. in a prompt convert 100 GBP to to USD GBP is base(Base currency)",
                    },
                    "target": {
                        "type": "string",
                        "description": "target currency code representing the currency into which the base amount will be converted. three-letter currency code supported by the ExchangeRate API (e.g., 'USD', 'INR', 'GBP') eg. in a prompt convert 100 GBP to to USD USD is target currency",
                    },
                    "amount": {
                        "type": "string",
                        "description": "The amount in the base currency to be converted.",
                    },
                },
                "required": ["base", "target", "amount"],
            },
        },
    ]
    
    try: 
        endpoint = "https://models.github.ai/inference"
        model_name = "openai/gpt-4o-mini"

        client = OpenAI(
            base_url=endpoint,
            api_key=GITHUB_TOKEN,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant",
                },
                {
                    "role": "user",
                    "content": f"{textbox_input}",
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            functions=functions,
        )

        # answer = response.choices[0].message.content
        return response
    except Exception as e:
        print(f"Exception {e} for {textbox_input}")


def run_pipeline(textbox_input):
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    # 1. Define a list of callable tools for the mode
    
    # if answer == 'True': #tool_calls
        
    #     get_exchange_rate()
    #     st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    # elif True: #tools not used
    #     # Update this
    #     st.write(f"(Function calling not used) and response from the model")
    # else:
    #     st.write("NotImplemented")

 # Title of the app
st.title("Multilingual Money Changer")

# Text box for user input
user_input = st.text_input("Enter the amount and the currency")

# Submit button
if st.button("Submit"):
    # Display the input text below the text box
    st.write(call_llm(user_input)) 
