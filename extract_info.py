import json
from llamaapi import LlamaAPI
import re

from generate_search_queries import generate_search_queries

# Initialize the SDK
llama = LlamaAPI("LL-tgPtDwuIROTSjbgSdqTk7vC0WT5VQZAjpaw1XSpNvpsZLdht1ANQeO7yLrV6MwCR")

def extract_budget_info(text):
    # Define the variables
    variables = {
        "number_of_participants": 0,
        "number_of_sites": 0,
        "trial_phase": "",
        "duration_months": 0,
        "protocol_complexity": "",
        "ethics_committee_approval_required": False,
        "regulatory_agency": "",
        "other_compliance_requirements": "",
        "site_fees_per_site": 0,
        "site_monitoring_frequency": "",
        "site_recruitment_strategies": "",
        "principal_investigator_salary": 0,
        "number_of_clinical_staff": 0,
        "clinical_staff_salary": 0,
        "staff_training_requirements": "",
        "advertising_and_outreach_budget": 0,
        "screening_cost_per_participant": 0,
        "retention_programs_and_incentives": "",
        "data_collection_tools_cost": 0,
        "data_monitoring_cost": 0,
        "statistical_analysis_cost": 0,
        "study_drug_and_placebo_cost": 0,
        "medical_equipment_cost": 0,
        "laboratory_test_cost_per_participant": 0,
        "participant_insurance_cost": 0,
        "investigator_insurance_cost": 0,
        "project_management_cost": 0,
        "facility_overheads": 0,
        "legal_and_contractual_costs": 0,
        "publication_cost": 0,
        "stakeholder_communication_cost": 0,
        "dissemination_activities_cost": 0
    }

    # Build the API request
    api_request_json = {
        "messages": [
            {
                "role": "system",
                "content": "You are an AI assistant specialized in extracting clinical trial budget information from text. Your task is to carefully analyze the given text and extract specific budget-related information. For each variable, provide the extracted value if available, or 'Not available' if the information is not present in the text. Be precise and avoid inferring information that is not explicitly stated."
            },
            {
                "role": "user",
                "content": f"Please extract the following budget information from the text. For each item, provide the exact value found in the text, or 'Not available' if the information is not present. Do not infer or estimate values.\n\n{json.dumps(variables, indent=2)}\n\nText: {text}"
            }
        ],
        "functions": [
            {
                "name": "update_budget_variables",
                "description": "Update the budget variables with extracted information",
                "parameters": {
                    "type": "object",
                    "properties": {var: {"type": "string"} for var in variables.keys()},
                    "required": list(variables.keys())
                }
            }
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }

    # Get the response from the LLM
    response = llama.run(api_request_json)
    response_json = response.json()

    # Extract the function call
    if 'function_call' in response_json['choices'][0]['message']:
        function_call = response_json['choices'][0]['message']['function_call']
        if function_call['name'] == 'update_budget_variables':
            extracted_data = function_call['arguments']
            
            # Update variables with extracted data
            for key, value in extracted_data.items():
                if isinstance(value, str) and value.strip().lower() != "not available":
                    if isinstance(variables[key], bool):
                        variables[key] = value.lower() == "true"
                    elif isinstance(variables[key], (int, float)):
                        try:
                            cleaned_value = value.replace('$', '').replace(',', '')
                            variables[key] = int(cleaned_value) if isinstance(variables[key], int) else float(cleaned_value)
                        except ValueError:
                            pass  # Keep the original value if conversion fails
                    else:
                        variables[key] = value
                elif isinstance(value, (int, float, bool)):
                    variables[key] = value

    # Generate search queries for missing data
    missing_data = {k: v for k, v in variables.items() if v == 0 or v == "" or v is False}
    completed_data = {k: v for k, v in variables.items() if v != 0 and v != "" and v is not False}

    return completed_data, missing_data





