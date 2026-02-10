from typing import Tuple, Dict
import dotenv
from dotenv import load_dotenv
import os
import requests
import json
import streamlit as st
import os
from openai import OpenAI
from langsmith import wrappers, tracable

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
os.environ['LANGCHAIN_TRACING_V2'] = True
LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = LANGSMITH_API_KEY
os.environ['LANGCHAIN_PROJECT'] = 'Moneychanger'

client = OpenAI(
    base_url=endpoint,
    api_key=GITHUB_TOKEN,
)

@tracable
def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    load_dotenv()
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}'
    response = requests.get(url)
    data = response.json()
    return (base, target, amount, f'{data["conversion_result"]:.2f}')

@tracable
def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    
    tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_exchange_rate",
                        "description": "Convert a given amount of money from one currency to another. Each currency will be represented as a 3-letter code",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "base": {
                                    "type": "string",
                                    "description": "The base or original currency.",
                                },
                                "target": {
                                    "type": "string",
                                    "description": "The target or converted currency",
                                },
                                "amount": {
                                    "type": "string",
                                    "description": "The amount of money to convert from the base currency.",
                                },
                            },
                            "required": ["base", "target", "amount"],
                            "additionalProperties": False,
                        },
                    },
                }
                ]

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
            tools=tools,
            # function_call="auto"
        )

    
    except Exception as e:
        print(f"Exception {e} for {textbox_input}")
    else:
        return response#.choices[0].message.content

@tracable
def run_pipeline(textbox_input):
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    response = call_llm(textbox_input)
    
    if response.choices[0].finish_reason == 'tool_calls':
        response_arument = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        base = response_arument['base']
        target = response_arument['target']
        amount = response_arument['amount']
        _, _, _, conversion_result = get_exchange_rate(base, target, amount)
        st.write(f'{base} {amount} is {target} {conversion_result}')

    elif response.choices[0].finish_reason == 'stop':
        st.write(f"(Function calling not used) and response from the model {response.choices[0].message.content}")
    else:
        st.write("NotImplemented")

 # Title of the app
st.title("Multilingual Money Changer")

# Text box for user input
user_input = st.text_input("Enter the amount and the currency")

# Submit button
if st.button("Submit"):
    # Display the input text below the text box
    st.write(run_pipeline(user_input)) 
