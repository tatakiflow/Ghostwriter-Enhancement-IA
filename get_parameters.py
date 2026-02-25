import requests
import os
from dotenv import load_dotenv

def get_params_from_ghostwritter():

  #Per silenciar el certificate requirement
  import urllib3
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  load_dotenv()

  url = os.getenv("GHOSTWRITER_UR")
  auth_token = os.getenv("GHOSTWRITER_API_TOKEN")

  #Verficació per verue si hi ha un auth code.

  if auth_token is None:
      exit("Error un finding a variable")

  #Es defineix la query

  body = """query MyQuery {
  finding(where: {title: {_nlike: "%[ERROR IA]"}) {
    title
    id
    description
     }
    }
    """

  #Request
  response = requests.post(url=url, 
                          json={"query": body},
                          headers={"content-type":"application/json", 
                                    "Authorization":f"Bearer {auth_token}"},                         
                          verify=False)

  response_data = response.json()

  #Llista buida a omplenar amb el titol de les vulns sense descripció
  vulns_to_enchance = []
  if "errors" in response_data:
      
      data_errors = response_data["errors"]
      print(data_errors)
      exit(1)

  elif "data" in response_data:
      
      vuln_titles = response_data["data"]["finding"]

      for desc in vuln_titles:
    
          description = desc["description"]
          if description == "<p xmlns=\"http://www.w3.org/1999/xhtml\"></p>" or description == "":
              vuln_data = {
                  "id": desc["id"],
                  "title": desc["title"]
              }
              vulns_to_enchance.append(vuln_data)
          
  
  return vulns_to_enchance          

    
        




