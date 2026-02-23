# Ghostwriter Enhancement IA

Automatiza la mejora de *findings* en Ghostwriter usando un modelo local de IA (Ollama), rellenando `description` y `mitigation` cuando están vacíos.

## ¿Qué hace este proyecto?

El flujo principal es:

1. Consulta Ghostwriter (GraphQL) y obtiene findings.
2. Filtra findings sin descripción útil.
3. Genera contenido técnico con IA (`description` y `mitigation`).
4. Actualiza cada finding en Ghostwriter mediante mutación GraphQL.

## Estructura

- `main.py`: orquesta el proceso completo.
- `get_parameters.py`: obtiene y filtra findings desde Ghostwriter.
- `data_enhancement.py`: genera descripción y mitigación con Ollama.
- `return_data.py`: envía la mutación para actualizar findings.

## Requisitos

- Python 3.10+
- Ghostwriter accesible en `https://127.0.0.1/v1/graphql`
- Token de API de Ghostwriter
- Ollama instalado y corriendo
- Modelo descargado en Ollama: `llama3.1`

## Instalación

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala dependencias:

```bash
pip install requests python-dotenv ollama urllib3
```

4. Descarga el modelo en Ollama (si aún no lo tienes):

```bash
ollama pull llama3.1
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
GHOSTWRITER_API_TOKEN=tu_token_aqui
```

## Ejecución

```bash
python main.py
```

## Notas importantes

- El proyecto usa `verify=False` en las peticiones HTTPS para entorno local/lab.
- Si Hasura responde con errores, se muestran por consola por ID de finding.
- La mutación actualiza los campos `description` y `mitigation`.

## Troubleshooting rápido

- **Token inválido o ausente**: revisa `GHOSTWRITER_API_TOKEN` en `.env`.
- **Ollama no responde**: verifica que el servicio esté activo (`ollama serve`) y que el modelo exista.
- **Error GraphQL**: confirma esquema de Ghostwriter/Hasura y permisos del token.


