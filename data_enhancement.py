from ollama import chat
from ollama import ChatResponse
from ollama import Client
import os
import json

def data_enhancement(title_list_for_ia):

    vulns_enhanced_ia = [] 

    client = Client(
    host= os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    
    for vuln in title_list_for_ia:

        id_original = vuln["id"] 
        title_original = vuln["title"]
        
        prompt = f"""Actúa como un analista de ciberseguridad nivel senior. Tu única tarea es extraer la información técnica de la vulnerabilidad indicada y estructurarla en un objeto JSON.
                Restricciones absolutas:
                1. Tu respuesta debe ser ÚNICA Y EXCLUSIVAMENTE un objeto JSON válido con exactamente dos claves en minúsculas: "description" y "mitigation".
                2. Prohibido envolver la respuesta en bloques de código Markdown (```json ... ```). Devuelve la estructura plana para su parseo directo.
                3. Prohibido añadir saludos, introducciones, confirmaciones de entendimiento o cualquier carácter que no forme parte del objeto JSON.
                4. El contenido de los valores debe mantener un rigor técnico absoluto, integrando tácticas, técnicas y mitigaciones de MITRE ATT&CK, clasificaciones CWE y lineamientos OWASP u OSSTMM aplicables.
                5. La longitud del texto para cada clave debe oscilar estrictamente entre 3 y 5 oraciones.
                6. En el campo "mitigacion", omite controles genéricos. Define la solución a nivel de arquitectura, segmentación, controles compensatorios o configuraciones precisas en los sistemas afectados.
                
                Vulnerabilidad objetivo: {vuln}"""
        
        try:
            response = client.chat(
                model='llama3.1',
                messages=[{'role':'user','content': prompt}],
                format='json'
                )
            
            print("[+] Generating response, please, wait.")

            resultats_ia = response['message']['content']
            resultats_json = json.loads(resultats_ia)    

            data_enhanced = {
                "id": id_original,
                "title": title_original,
                "description": resultats_json["description"],
                "mitigation": resultats_json["mitigation"]
            }

            vulns_enhanced_ia.append(data_enhanced)
        
        except Exception as e:
            print(f"[-] Error processing {vuln}: {e}")
        
    return vulns_enhanced_ia
