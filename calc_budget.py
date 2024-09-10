def calculate_total_budget(budget_factors):
    # Extract values from the dictionary
    number_of_participants = budget_factors.get("number_of_participants", 0)
    number_of_sites = budget_factors.get("number_of_sites", 0)
    principal_investigator_salary = budget_factors.get("principal_investigator_salary", 0)
    number_of_clinical_staff = budget_factors.get("number_of_clinical_staff", 0)
    clinical_staff_salary = budget_factors.get("clinical_staff_salary", 0)
    site_fees_per_site = budget_factors.get("site_fees_per_site", 0)
    screening_cost_per_participant = budget_factors.get("screening_cost_per_participant", 0)
    laboratory_test_cost_per_participant = budget_factors.get("laboratory_test_cost_per_participant", 0)
    participant_insurance_cost = budget_factors.get("participant_insurance_cost", 0)
    investigator_insurance_cost = budget_factors.get("investigator_insurance_cost", 0)
    advertising_and_outreach_budget = budget_factors.get("advertising_and_outreach_budget", 0)
    data_collection_tools_cost = budget_factors.get("data_collection_tools_cost", 0)
    data_monitoring_cost = budget_factors.get("data_monitoring_cost", 0)
    statistical_analysis_cost = budget_factors.get("statistical_analysis_cost", 0)
    study_drug_and_placebo_cost = budget_factors.get("study_drug_and_placebo_cost", 0)
    medical_equipment_cost = budget_factors.get("medical_equipment_cost", 0)
    project_management_cost = budget_factors.get("project_management_cost", 0)
    facility_overheads = budget_factors.get("facility_overheads", 0)
    legal_and_contractual_costs = budget_factors.get("legal_and_contractual_costs", 0)
    publication_cost = budget_factors.get("publication_cost", 0)
    stakeholder_communication_cost = budget_factors.get("stakeholder_communication_cost", 0)
    dissemination_activities_cost = budget_factors.get("dissemination_activities_cost", 0)
    
    # Calculate costs related to participants and sites
    participant_related_costs = (
        screening_cost_per_participant * number_of_participants +
        laboratory_test_cost_per_participant * number_of_participants +
        participant_insurance_cost * number_of_participants
    )
    
    site_related_costs = (
        site_fees_per_site * number_of_sites
    )
    
    # Calculate costs related to investigator and staff
    staff_related_costs = (
        principal_investigator_salary +
        clinical_staff_salary * number_of_clinical_staff +
        investigator_insurance_cost
    )
    
    # Calculate total budget by summing all relevant costs
    total_budget = (
        participant_related_costs +
        site_related_costs +
        staff_related_costs +
        advertising_and_outreach_budget +
        data_collection_tools_cost +
        data_monitoring_cost +
        statistical_analysis_cost +
        study_drug_and_placebo_cost +
        medical_equipment_cost +
        project_management_cost +
        facility_overheads +
        legal_and_contractual_costs +
        publication_cost +
        stakeholder_communication_cost +
        dissemination_activities_cost
    )
    
    return total_budget
