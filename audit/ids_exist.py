import requests

agency_url = "http://microservice-b:8001/"
process_url = "http://microservice-a:8000/"

def check_process_id(process_id: int) -> bool:
    process_response = requests.get(process_url)
    process_json = process_response.json()
    x = []
    
    for i in process_json.values():
        for j in i:
            x.append(j["process_id"])
    
    if process_response.status_code != 200:
        return False
    return process_id in x

def check_agency_id(agency_id: int) -> bool:
    agency_response = requests.get(agency_url)
    agency_json = agency_response.json()
    x = []
    
    for i in agency_json.values():
        for j in i:
            x.append(j["agency_id"])
    
    if agency_response.status_code != 200:
        return False
    
    return agency_id in x

