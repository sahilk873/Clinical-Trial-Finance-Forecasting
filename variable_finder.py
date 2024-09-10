import json
from openai import OpenAI

# Initialize the SDK
client = OpenAI(api_key="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")

def determine_variable_value(variable_name, original_context, scraped_info):
    # Build the API request
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant specialized in determining values for clinical trial variables. Your task is to analyze the given information and determine a value for the specified variable. If this is the case, you should only return those two values, no additional text."
        },
        {
            "role": "user",
            "content": f"""Please determine the value for the variable '{variable_name}' based on the following information:

Original Context:
{original_context}

Scraped Information:
{scraped_info}

Return the value and confidence level as two values separated by a comma (e.g., 1000,0.3 for a value of 1000 with 30% confidence) with no other text.
"""
        }
    ]

    # Get the response from the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.1,
        max_tokens=500
    )
    
    # Extract the content from the response
    content = response.choices[0].message.content
    if content == "NONE":
        return None, 0

    # Split the content into value and confidence
    value, confidence = content.strip().split(',')

    # Convert confidence to float
    confidence = float(confidence)
    
    # If value is numeric, convert to int
    if value.isdigit():
        value = int(value)
    # If value is 'NONE', set it to None
    elif value.upper() == 'NONE':
        value = None

    return value, confidence

'''# Example usage
variable_name = "number_of_participants"
original_context = """
Our clinical trial is a Phase II study investigating a new treatment for type 2 diabetes. 
We're planning to conduct the trial across multiple sites in the United States. 
The duration of the trial is expected to be 18 months.
"""
scraped_info = """
Recent Phase II diabetes studies have typically included between 100 to 500 participants.
A similar study conducted last year by PharmaCorp included 250 participants across 10 sites.
The average number of participants for Phase II diabetes trials in the past 5 years is 300.
"""

value, confidence = determine_variable_value(variable_name, original_context, scraped_info)

print(f"Value: {value}")
print(f"Confidence: {confidence}")

'''



'''import json
from llamaapi import LlamaAPI

# Initialize the SDK
llama = LlamaAPI("LL-tgPtDwuIROTSjbgSdqTk7vC0WT5VQZAjpaw1XSpNvpsZLdht1ANQeO7yLrV6MwCR")

def determine_variable_value(variable_name, original_context, scraped_info):
    # Build the API request
    api_request_json = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant specialized in determining values for clinical trial variables. Your task is to analyze the given information and determine a value for the specified variable. If this is the case, you should only return those two values, no additional text. If a value cannot be determined with confidence, you should return NONE."
            },
            {
                "role": "user",
                "content": f"""Please determine the value for the variable '{variable_name}' based on the following information:

Original Context:
{original_context}

Scraped Information:
{scraped_info}

If you cannot determine a value with confidence, return NONE,0. Otherwise, return the value and confidence level as two values separated by a comma (e.g., 300,0.8 for a value of 300 with 80% confidence) with no other text.
"""
            }
        ],
        "temperature": 0.1,
        "max_tokens": 500
    }

    # Get the response from the LLM
    response = llama.run(api_request_json)
    
    # Parse the JSON response
    response_json = response.json()

    # Extract the content from the response
    content = response_json['choices'][0]['message']['content']

    # Split the content into value and confidence
    value, confidence = content.strip().split(',')

    # Convert confidence to float
    confidence = float(confidence)
    if value.isdigit():
        value = int(value)

    # If value is 'NONE', set it to None
    if not value.isdigit():
        if value.upper() == 'NONE':
          value = None

    return value, confidence

# Example usage
variable_name = "number_of_participants"
original_context = """
Our clinical trial is a Phase II study investigating a new treatment for type 2 diabetes. 
We're planning to conduct the trial across multiple sites in the United States. 
The duration of the trial is expected to be 18 months.
"""
scraped_info = """
Recent Phase II diabetes studies have typically included between 100 to 500 participants.
A similar study conducted last year by PharmaCorp included 250 participants across 10 sites.
The average number of participants for Phase II diabetes trials in the past 5 years is 300.
"""

value, confidence = determine_variable_value(variable_name, original_context, scraped_info)

print(f"Value: {value}")
print(f"Confidence: {confidence}")



'''