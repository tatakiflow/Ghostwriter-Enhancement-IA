# Ghostwriter Enhancement IA

Automatiza la mejora de *findings* en Ghostwriter usando un modelo local de IA (Ollama), rellenando `description` y `mitigation` cuando están vacíos.

## ¿Qué hace este proyecto?

El flujo principal es:

1. Consulta Ghostwriter (GraphQL) y obtiene findings.
2. Filtra findings sin descripción útil.
3. Genera contenido técnico con IA (`description` y `mitigation`).
4. Actualiza cada finding en Ghostwriter mediante mutación GraphQL.
5. El proceso se ejecuta automáticamente cada hora mediante un *scheduler*.

## Estructura

- `main.py`: orquesta el proceso completo y ejecuta el *scheduler*.
- `get_parameters.py`: obtiene y filtra findings desde Ghostwriter.
- `data_enhancement.py`: genera descripción y mitigación con Ollama.
- `return_data.py`: envía la mutación para actualizar findings.
- `docker-compose.yml` y `Dockerfile`: permiten desplegar el proyecto en un contenedor Docker.

## Requisitos

- Python 3.10+ (si se ejecuta localmente)
- Docker y Docker Compose (si se ejecuta en contenedor)
- Ghostwriter accesible
- Token de API de Ghostwriter
- Ollama instalado y corriendo (en la máquina host o accesible por red)
- Modelo descargado en Ollama: `llama3.1`

## Instalación y Ejecución

### Opción 1: Usando Docker (Recomendado)

1. Clona el repositorio.
2. Crea un archivo `.env` en la raíz del proyecto con tus variables:
   ```env
   GHOSTWRITER_URL=tu_url_aqui
   GHOSTWRITER_API_TOKEN=tu_token_aqui
   ```
3. Levanta el contenedor:
   ```bash
   docker-compose up -d
   ```
   *Nota: El `docker-compose.yml` ya está configurado para conectarse a una instancia local de Ollama en la máquina host usando `host.docker.internal`.*

### Opción 2: Ejecución Local (Python)

1. Clona el repositorio.
2. Crea y activa un entorno virtual.
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Descarga el modelo en Ollama (si aún no lo tienes):
   ```bash
   ollama pull llama3.1
   ```
5. Crea un archivo `.env` en la raíz del proyecto:
   ```env
   GHOSTWRITER_URL=tu_url_aqui
   GHOSTWRITER_API_TOKEN=tu_token_aqui
   OLLAMA_HOST=http://localhost:11434 # Opcional, por defecto es localhost
   ```
6. Ejecuta el script:
   ```bash
   python main.py
   ```

## Notas importantes

- El proyecto usa `verify=False` en las peticiones HTTPS para entorno local/lab.
- Si Hasura responde con errores, se muestran por consola por ID de finding.
- La mutación actualiza los campos `description` y `mitigation`.
- El script principal (`main.py`) se queda corriendo en bucle y ejecuta la tarea cada hora.

## Troubleshooting rápido

- **Token inválido o ausente**: revisa `GHOSTWRITER_API_TOKEN` en `.env`.
- **Ollama no responde**: verifica que el servicio esté activo (`ollama serve`) y que el modelo exista. Si usas Docker, asegúrate de que Ollama permite conexiones externas si es necesario.
- **Error GraphQL**: confirma esquema de Ghostwriter/Hasura y permisos del token.


