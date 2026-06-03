# AstroData Backend

Backend de AstroData Lab construido con FastAPI.

## Configuracion local

Requisitos instalados en la maquina:

- Python 3.13 o compatible.
- MongoDB Community Server corriendo en `mongodb://localhost:27017/`.
- Ollama para ejecutar el LLM local.
- Modelo de Ollama `llama3.2`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` con tu configuracion local:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=astrodata_lab

OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT_SECONDS=180

NASA_API_KEY=TU_API_KEY_DE_NASA
APOD_SEED_LIMIT=100
```

`NASA_API_KEY=DEMO_KEY` funciona para pruebas pequenas, pero suele fallar con `HTTP 429 Too Many Requests`.

Las dependencias de embeddings se instalan aparte:

```powershell
pip install -r requirements-ml.txt
```

`requirements-ml.txt` usa `fastembed`, evitando la instalacion pesada de PyTorch.

## Requisito para Consulta IA: Ollama

La seccion **Consulta IA** necesita Ollama corriendo localmente. Si Ollama no esta disponible, el backend responde `503 Service Unavailable`.

Instala Ollama desde:

```txt
https://ollama.com
```

Descarga el modelo configurado en `.env`:

```powershell
ollama pull llama3.2
```

Verifica que exista:

```powershell
ollama list
```

Levanta Ollama si no esta corriendo:

```powershell
ollama serve
```

Si `ollama serve` responde que el puerto `11434` ya esta en uso, significa que Ollama ya esta corriendo.

Prueba una generacion:

```powershell
ollama run llama3.2
```

Dentro del chat interactivo de Ollama puedes salir escribiendo:

```txt
/bye
```

Nota: `/bye` solo funciona dentro de `ollama run`, no en PowerShell normal.

## Ejecutar servidor

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Usa `python -m uvicorn` desde el `.venv` para evitar ejecutar un `uvicorn` global sin dependencias como `motor`.

Endpoints iniciales:

- `GET /api/health`
- `GET /api/status`
- `GET /api/db/ping`
- `POST /api/db/query`
- `GET /api/stats`
- `GET /api/objetos-celestes`
- `POST /api/objetos-celestes`
- `GET /api/objetos-celestes/{objeto_id}`
- `PUT /api/objetos-celestes/{objeto_id}`
- `DELETE /api/objetos-celestes/{objeto_id}`
- `GET /api/documentos`
- `POST /api/documentos`
- `GET /api/documentos/{documento_id}`
- `PUT /api/documentos/{documento_id}`
- `DELETE /api/documentos/{documento_id}`
- `GET /api/documentos/{documento_id}/chunks`
- `POST /api/chunks`
- `GET /api/chunks/{chunk_id}`
- `PUT /api/chunks/{chunk_id}`
- `DELETE /api/chunks/{chunk_id}`
- `GET /api/busqueda?q=...`
- `POST /api/chat/preguntar`
- `GET /api/chat/historial`
- `DELETE /api/chat/historial`

## Seed de objetos celestes

Despues de configurar `MONGODB_URI` en `.env`, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m app.seed.seed_objetos_celestes
```

El seed inicial carga objetos astronomicos base en la coleccion `celestial_objects`.

## Crear indices

Despues de configurar `MONGODB_URI` en `.env`, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m app.seed.crear_indices
```

El script crea indices normales para `celestial_objects`, `documents`, `document_chunks` y `query_history`. Tambien imprime la definicion del indice de MongoDB Atlas Vector Search para `document_chunks.embedding`.

El archivo de referencia del indice vectorial esta en:

```text
app/seed/atlas_vector_search_index.json
```

## Seed APOD, chunks y embeddings

APOD alimenta las colecciones documentales usadas por el RAG:

- `documents`
- `document_chunks`

Primero descarga/actualiza documentos APOD y genera chunks:

```powershell
.\.venv\Scripts\python.exe -m app.seed.seed_apod_documentos
```

Luego genera embeddings para los chunks sin embedding:

```powershell
.\.venv\Scripts\python.exe -m app.seed.generar_embeddings_chunks
```

Este proceso usa `sentence-transformers/all-MiniLM-L6-v2` mediante `fastembed` para completar el campo `embedding` de cada documento en `document_chunks`. El modelo genera vectores de 384 dimensiones.

En MongoDB local, el chat usa un fallback de similitud coseno en Python. En MongoDB Atlas, puede usar Atlas Vector Search con el indice definido en `app/seed/atlas_vector_search_index.json`.

Si NASA responde `HTTP 429 Too Many Requests`, configura una API key propia en `.env`:

```env
NASA_API_KEY=TU_API_KEY_DE_NASA
```

Tambien puedes bajar temporalmente:

```env
APOD_SEED_LIMIT=30
```

## Flujo recomendado de preparacion

```powershell
.\.venv\Scripts\python.exe -m app.seed.crear_indices
.\.venv\Scripts\python.exe -m app.seed.seed_objetos_celestes
.\.venv\Scripts\python.exe -m app.seed.seed_apod_documentos
pip install -r requirements-ml.txt
.\.venv\Scripts\python.exe -m app.seed.generar_embeddings_chunks
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Antes de usar `POST /api/chat/preguntar`, verifica:

- `GET /api/db/ping` responde con `conectado: true`.
- `GET /api/stats` muestra documentos, chunks y chunks con embedding.
- Ollama responde en `http://127.0.0.1:11434/api/tags`.
- `OLLAMA_MODEL` coincide con un modelo listado por `ollama list`.

Con MongoDB local no necesitas Atlas Vector Search para la demo: el backend usa fallback local con similitud coseno. Si despliegas en MongoDB Atlas, configura el indice vectorial usando `app/seed/atlas_vector_search_index.json`.

## Terminal de BD

`POST /api/db/query` permite consultas controladas sobre MongoDB para la seccion administrativa. Soporta:

- `find`
- `aggregate`
- `count_documents`

Solo permite las colecciones del proyecto y bloquea operadores peligrosos como `$where`, `$function`, `$out` y `$merge`.

## Diagnostico rapido

Verificar que el backend importa correctamente:

```powershell
.\.venv\Scripts\python.exe -c "import app.main; print('app import ok')"
```

Verificar que Ollama responde:

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

Si Consulta IA devuelve `503`, revisa:

- Ollama esta corriendo.
- `.env` tiene `OLLAMA_BASE_URL=http://127.0.0.1:11434`.
- `.env` tiene `OLLAMA_MODEL=llama3.2`.
- `.env` tiene `OLLAMA_TIMEOUT_SECONDS=180` si el modelo tarda mas de un minuto.
- `ollama list` muestra ese modelo.

## Ejecutar pruebas

```powershell
pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

## Estructura

- `app/api`: rutas HTTP.
- `app/core`: configuracion global.
- `app/db`: conexion a bases de datos.
- `app/models`: modelos internos del dominio.
- `app/schemas`: DTOs de entrada/salida.
- `app/repositories`: acceso a datos.
- `app/services`: logica de negocio.
- `app/use_cases`: casos de uso de la aplicacion.
- `app/rag`: componentes del pipeline RAG.
- `app/seed`: scripts de poblacion inicial.
