import json
from llamaapi import LlamaAPI
import requests

# Initialize the SDK
llama = LlamaAPI("LL-tgPtDwuIROTSjbgSdqTk7vC0WT5VQZAjpaw1XSpNvpsZLdht1ANQeO7yLrV6MwCR")

def get_forex_price(base_currency, quote_currency):
    url = f"https://v6.exchangerate-api.com/v6/80adb8b77dd3771dc7c6bfb3/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return f"The exchange rate is 1 {base_currency} = {data['conversion_rates'].get(quote_currency)} {quote_currency}"

# Build the API request
api_request_json = {
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant that provides information about currency exchange rates. When given information about exchange rates, incorporate it into your response and provide a clear explanation."
        },
        {"role": "user", "content": "What is the current exchange rate of USD to EUR?"}
    ],
    "max_length": 500,
    "temperature": 0.1,
    "top_p": 1.0,
    "frequency_penalty": 1.0,
    "functions": [
        {
            "name": "get_forex_price",
            "description": "Get the current exchange rate between two currencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_currency": {
                        "type": "string",
                        "description": "The base currency code (e.g., USD)"
                    },
                    "quote_currency": {
                        "type": "string",
                        "description": "The quote currency code (e.g., EUR)"
                    }
                },
                "required": ["base_currency", "quote_currency"]
            }
        }
    ]
}

response = llama.run(api_request_json)
response_json = response.json()

# Check if the LLM wants to call the function
if 'function_call' in response_json['choices'][0]['message']:
    function_call = response_json['choices'][0]['message']['function_call']
    if function_call['name'] == 'get_forex_price':
        args = function_call['arguments']
        forex_price = get_forex_price(args['base_currency'], args['quote_currency'])
        
        # Send the function result back to the LLM
        api_request_json['messages'].append({
            "role": "function",
            "name": "get_forex_price",
            "content": forex_price
        })
        api_request_json['messages'].append({
            "role": "user",
            "content": "Please provide a response based on the exchange rate information."
        })
        
        print(api_request_json)
        
        del api_request_json['functions']
        
        # Get the final response from the LLM
        final_response = llama.run(api_request_json)
        final_response_json = final_response.json()
        final_chatbot_response = final_response_json['choices'][0]['message']['content']
        
        print(final_chatbot_response)