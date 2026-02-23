import requests
import os
from dotenv import load_dotenv
import urllib3

def mutate_parameters(titles_enhanced):

    #Per silenciar el certificate requirement
   
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()

    url = "https://127.0.0.1/v1/graphql"
    auth_token = os.getenv("GHOSTWRITER_API_TOKEN")

    for vuln in titles_enhanced:

        finding_id = vuln["id"]
        title = vuln["title"]
        description = vuln["description"]
        mitigation = vuln["mitigation"]

        mutation_graphql = """
        mutation MyMutation($id: bigint!, $description: String!, $mitigation: String!) {
            update_finding(where: {id: {_eq: $id}}, _set: {description: $description, mitigation: $mitigation}) {
                affected_rows
            }
        }
        """

        #Diccionari de variables
        variables_graphql = {
            "id": int(finding_id),
            "description": description,
            "mitigation": mitigation
        }

        payload = {
            "query": mutation_graphql,
            "variables": variables_graphql
        }

        try:

            response = requests.post(url=url,
                        json=payload,
                        headers={"content-type":"application/json",
                                "Authorization":f"Bearer {auth_token}"},
                        verify=False)

            res_json = response.json()

            if "errors" in res_json:
                print(f"[-] Hasura rejected the mutation for ID {finding_id}: {res_json['errors']}")
            else:
                print(f"[+] Finding '{title}' (ID: {finding_id}) correctly updated in Ghostwriter.")

        except Exception as e:

            print(f"Error updating finding {finding_id}: {e}")

    return True