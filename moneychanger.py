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
            model=model_name
        )

        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(f"Exception {e} for {textbox_input}")


def run_pipeline(textbox_input):
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""
     
    # try:
        
    #     endpoint = "https://models.github.ai/inference"
    #     model_name = "openai/gpt-4o-mini"

    #     client = OpenAI(
    #         base_url=endpoint,
    #         api_key=GITHUB_TOKEN,
    #     )

    #     response = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": f"You are a helpful assistant to determine whether the user query {textbox_input} is a currency conversion" 
    #                 "query or not if the {textbox_input} has mention of conversion from one currency to another the answer will be True else it's false"
    #                 "the {textbox_input} may not explicitely mention 2 currencies(eg. EUR and USD),rather it may indicate name of 2 countries"
    #                 "eg. what is the value of 250 EUR in Newyork money means a conversion from EUR to USD. The user query {textbox_input} may be in other languages"
    #                 "than English. Your answer will be in Boolean True and False"
    #             },
    #             {
    #                 "role": "user",
    #                 "content": f"{textbox_input}",
    #             }
    #         ],
    #         temperature=1.0,
    #         top_p=1.0,
    #         max_tokens=1000,
    #         model=model_name
    #     )

    #     answer = response.choices[0].message.content

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
