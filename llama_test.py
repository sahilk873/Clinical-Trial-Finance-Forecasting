import json
from llamaapi import LlamaAPI

# Initialize the SDK
llama = LlamaAPI("LL-tgPtDwuIROTSjbgSdqTk7vC0WT5VQZAjpaw1XSpNvpsZLdht1ANQeO7yLrV6MwCR")

# Build the API request
api_request_json = {
    "messages": [ 
        {"role": "user", "context": "Answer all questions given?", "content": "What is the meaning of life and what is the capital of Paris?"}
    ],
   "max_length": 500,
   "temperature": 0.1,
   "top_p": 1.0,
   "frequency_penalty": 1.0 
}

response = llama.run(api_request_json)
response_json = response.json()
chatbot_response = response_json['choices'][0]['message']['content']

print(chatbot_response)
