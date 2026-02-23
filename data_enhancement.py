from ollama import chat
import json

def data_enhancement(title_list_for_ia):

    resultats_ia = []

    for title in title_list_for_ia:
        
        prompt = f"""Actúa como un analista de ciberseguridad nivel senior. Tu única tarea es extraer la información técnica de la vulnerabilidad indicada y estructurarla en un objeto JSON.
                Restricciones absolutas:
                1. Tu respuesta debe ser ÚNICA Y EXCLUSIVAMENTE un objeto JSON válido con exactamente dos claves en minúsculas: "descripcion" y "mitigacion".
                2. Prohibido envolver la respuesta en bloques de código Markdown (```json ... ```). Devuelve la estructura plana para su parseo directo.
                3. Prohibido añadir saludos, introducciones, confirmaciones de entendimiento o cualquier carácter que no forme parte del objeto JSON.
                4. El contenido de los valores debe mantener un rigor técnico absoluto, integrando tácticas, técnicas y mitigaciones de MITRE ATT&CK, clasificaciones CWE y lineamientos OWASP u OSSTMM aplicables.
                5. La longitud del texto para cada clave debe oscilar estrictamente entre 3 y 5 oraciones.
                6. En el campo "mitigacion", omite controles genéricos. Define la solución a nivel de arquitectura, segmentación, controles compensatorios o configuraciones precisas en los sistemas afectados.

                Vulnerabilidad objetivo: {title}"""
        try:
            response = chat(
                model='llama3.1:8b',
                messages=[{'role':'user','content': prompt}],
                format='json'
                )
            
            diccionari_ia = json.loads(response.message.content)
            
            

            resultats_ia.append(response)

        except Exception as e:
            print(f"Error processing {title}: {e}")
        
    return response
