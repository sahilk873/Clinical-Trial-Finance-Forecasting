import json
from llamaapi import LlamaAPI
import re
llama = LlamaAPI("LL-tgPtDwuIROTSjbgSdqTk7vC0WT5VQZAjpaw1XSpNvpsZLdht1ANQeO7yLrV6MwCR")


def generate_search_queries(context, missing_data):
    # Prepare the input for the LLM
    missing_data_str = "\n".join([f"- {k.replace('_', ' ')}" for k in missing_data.keys()])
    #missing_data_str = "\n".join([k for k in missing_data.keys()])
    
    api_request_json = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant tasked with generating Google search queries to find missing information about a clinical trial budget. Based on the given context and list of missing data points, create one specific and targeted search query for each missing data point that are likely to yield the required information. The responses should be formatted like this: {missing data: query}. Make sure to include brackets around the missing data and query pairs "
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nMissing information:\n{missing_data_str}\n\nGenerate a Google search query for each missing piece of information. The queries should be specific to clinical trials and budget planning."
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }

    # Get the response from the LLM
    response = llama.run(api_request_json)
    response_json = response.json()

    # Extract the generated search queries
    generated_queries = response_json['choices'][0]['message']['content'].split('\n')


    # Join the list into a single string
    data_str = ' '.join(generated_queries)

    # Regex to match keys and values within brackets
    pattern = re.compile(r'\[(.*?):\s*"(.*?)"\]')

    # Find all matches
    matches = pattern.findall(data_str)

    # Convert matches to dictionary with each missing data type as key and its query as value
    search_queries = {key.strip(): value.strip() for key, value in matches}
    return search_queries

    
    
    