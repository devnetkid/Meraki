"""For a given organization, loop through each network name and search it for
the specified search string. Return a list of networks where a match was 
found. Write the results to a file.

REQUIREMENTS: pip install requests
Define your meraki evironment key as MERAKI_DASHBOARD_API_KEY or modify script
Tested with Python 3.11.2

DATE: 4/30/2023

"""

import csv
import os
import sys
import requests


def get_orgs(base_url, headers):
    """Get a list of organizations

    ARGS:
        base_url (str): The url common to all requests
        headers (dict): The headers as required by the API
    RETURNS:
        list: The list of organizations
    """
    url = base_url + 'organizations'
    response = requests.request('GET', url, headers=headers, timeout=3)
    if response.ok:
        return response.json()

    sys.exit(str(response.status_code) + ' ' + response.reason + ' ' + response.text)


def search_networks(base_url, headers, org_id, search_string):
    """Search for networks that contain the given search_string

    ARGS:
        base_url (str): The url common to all requests
        headers (dict): The headers as required by the API
        org_id (str): The organization ID to be searched
        search_string (str): The string of text to search for
    RETURNS:
        list: The list of networks that matched
    """
    url = base_url + f"organizations/{org_id}/networks"
    response = requests.request('GET', url, headers=headers, timeout=3)
    networks = response.json()
    networks_list = []
    for network in networks:
        if search_string.lower() in network['name'].lower():
            networks_list.append(network)
    return networks_list


def write_to_file(filename, networks):
    """Write the matched networks to a file
    
    ARGS:
        networks (list): The list of networks found in the search
    RETURNS:
        None
    """
    with open(filename, 'w', newline='', encoding='utf-8') as net_data:
        writer = csv.writer(net_data, delimiter=',')
        for network in networks:
            writer.writerow([network['id'],network['name']])


def main():
    """Primary function called when executing this script

    """
    # UPDATE THESE SETTINGS AS DESIRED
    search_string = 'abc'
    filename = "networks.csv"

    # MERAKI DASHBOARD SETTINGS
    base_url = "https://api.meraki.com/api/v1/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": os.environ.get('MERAKI_DASHBOARD_API_KEY')
    }

    orgs = get_orgs(base_url, headers)
    for num, org in enumerate(orgs):
        print(str(num) + ' - ' + org['name'])
    selected_org = input("\nSelect the organization to be searched: ")
    print(f"Searching the {orgs[int(selected_org)]['name']} organization")
    org_id = orgs[int(selected_org)]['id']
    search_results = search_networks(base_url, headers, org_id, search_string)
    print(f"Found {len(search_results)} entries with the string {search_string}")
    write_to_file(filename, search_results)
    print(f"The networks found have been written to the file {filename}")


if __name__ == '__main__':
    main()
