import json
from llamaapi import LlamaAPI
import re
from extract_info import extract_budget_info
import variables
from generate_search_queries import generate_search_queries
from google_search import return_url
from scraper_sel import scrape_text_from_url_sel
from scraper_bs import scrape_text_from_url_bs
from variable_finder import determine_variable_value
from scraper_scrapy import scrape_text_from_url_scrapy
from calc_budget import calculate_total_budget


def keep_letters_and_underscores(s):
    return re.sub(r'[^a-zA-Z_]', '', s)



sample_text_1 = """Our clinical trial, based in New York City, aims to evaluate the efficacy of a new drug for treating prostate cancer. The trial is a multi-center Phase II study involving 150 participants across 8 different sites and is expected to last for 12 months. The protocol is moderately complex, requiring participants to visit the site every two months for detailed assessments and various procedures.

We have obtained ethics committee approval and the trial will be conducted under the oversight of the FDA. Additional compliance requirements include regular safety reporting and periodic audits. The estimated site fees are $30,000 per site, with site monitoring visits scheduled on a monthly basis. Recruitment will focus on major hospitals and specialized cancer treatment centers in New York City.

The principal investigator's salary is estimated at $170,000. For patient recruitment and retention, we have allocated a budget of $50,000 for advertising and outreach. Retention programs will include regular follow-up calls.

Data management will utilize a comprehensive electronic data capture system. Clinical supplies will include study drugs and placebos costing approximately $110,000. Each participant will also require laboratory tests, estimated at $1,100 per participant.

We have budgeted $20,000 for participant insurance. Administrative costs include $50,000 for project management and $30,000 for facility overheads. For communication and reporting, we expect publication costs to be around $11,000, with stakeholder communication costs projected at $5,000. Dissemination activities, such as conferences and workshops, are estimated to cost $9,000.

The trial is specifically focused on advanced prostate cancer patients who have not responded to conventional treatments. The aim is to determine whether the new drug can reduce tumor size and improve patient quality of life. All participating sites are equipped with state-of-the-art facilities for comprehensive cancer care, and the principal investigator has extensive experience in oncology trials.

"""



def main():
    
    scrapes_per_variable = 3
    context = sample_text_1
    extracted_variables, missing_data = extract_budget_info(context)
    found_variables = dict()
    search_queries = generate_search_queries(context, missing_data)
    url_search_set = dict()
    
    for k, v in search_queries.items():
        k = k.lower().replace(" ", "_")
        k = keep_letters_and_underscores(k)
        url_search_set[k] = return_url(v, scrapes_per_variable)
        

    print("Extracted Variables:")
    for key, value in extracted_variables.items():
        #variables.key = value
        print(f"{key}: {value}")

    print("\nGoogle Search Queries for Missing Data:")
    for key, query in search_queries.items():
        print(f"{key}: {query}")
        
    
    for variable in missing_data:
        url_set = url_search_set[variable]
        value_confidence = {}
        for url in url_set:
            print("Scraping URL:", url)
            text = scrape_text_from_url_scrapy(url)
            if text:
                value, confidence = determine_variable_value(variable, context, text)
                value_confidence[confidence] = value
        found_variables[variable] = value_confidence[max(value_confidence.keys())]
    
    all_variables = extracted_variables.update(found_variables)
        
    budget = calculate_total_budget(all_variables)
    
    return budget
        
    
          
main()
















sample_text_2 = """Our clinical trial, based in Los Angeles, aims to evaluate the effectiveness of a new therapy for treating chronic migraines. This multi-center Phase III study will involve 120 participants across 6 different sites and is expected to last for 14 months. The protocol is relatively complex, requiring participants to visit the site every six weeks for comprehensive assessments and specific procedures.

Ethics committee approval has been obtained, and the trial will be conducted under the guidance of the EMA. Compliance requirements include regular data submissions and periodic site audits. Estimated site fees are $28,000 per site, with site monitoring visits scheduled on a bi-monthly basis. Recruitment will focus on large metropolitan hospitals and specialized neurology clinics in Los Angeles.

We will employ 12 clinical staff members, each with an estimated annual salary of $82,000. Staff training will include both initial protocol training and ongoing refresher courses. For patient recruitment and retention, we have set aside a budget of $55,000 for advertising and outreach, with an estimated screening cost of $700 per participant. Retention efforts will involve regular follow-up calls and transportation reimbursement.

Data management will leverage a modern electronic data capture system, costing approximately $12,000, with projected data monitoring expenses of $22,000. Statistical analysis costs are estimated at $32,000. Clinical supplies, including study drugs and placebos, are expected to cost $115,000. Laboratory tests for each participant are estimated at $1,150.

Participant insurance is estimated to cost $22,000. Administrative costs will include $52,000 for project management and $32,000 for facility overheads. Legal and contractual costs are anticipated to be around $18,000. Communication and reporting expenses include $10,000 for publications and $6,000 for stakeholder communication, with an additional $8,000 for dissemination activities such as conferences and workshops.

The trial is specifically designed for patients suffering from chronic migraines who have not found relief with conventional treatments. The goal is to determine if the new therapy can significantly reduce the frequency and severity of migraine attacks. All participating sites are well-equipped with advanced neurology facilities, and the principal investigator has a strong background in clinical neurology trials.

"""

sample_text_3 = """Our clinical trial, based in Chicago, aims to evaluate the safety and efficacy of a new vaccine for respiratory infections. This is a Phase I study involving 80 participants at a single site and is expected to last for 9 months. The protocol involves intensive monitoring, requiring participants to visit the site every two weeks for thorough assessments and various procedures.

Ethics committee approval has been obtained, and the trial will be conducted under the oversight of the FDA. Compliance requirements include detailed regulatory submissions and regular site inspections. The estimated site fees are $40,000, with site monitoring visits scheduled on a bi-weekly basis. Recruitment will focus on major hospitals and community health centers in Chicago.

The principal investigator's salary is estimated at $150,000. For patient recruitment and retention, we have allocated a budget of $40,000 for advertising and outreach. Retention programs will include regular follow-up calls and travel compensation.

Data management will utilize an advanced electronic data capture system costing $18,000, with projected data monitoring expenses of $20,000. Clinical supplies will include study vaccines costing approximately $90,000. Each participant will also require laboratory tests, estimated at $1,000 per participant.

We have budgeted $15,000 for participant insurance. Administrative costs include $45,000 for project management and $25,000 for facility overheads. For communication and reporting, we expect publication costs to be around $9,000, with stakeholder communication costs projected at $4,000. Dissemination activities, such as conferences and workshops, are estimated to cost $7,000.

The trial focuses on individuals at high risk of respiratory infections, particularly those with pre-existing conditions. The aim is to assess whether the new vaccine can effectively prevent infections and improve overall respiratory health. The trial site is equipped with state-of-the-art medical facilities, and the principal investigator has extensive experience in vaccine trials.

"""
