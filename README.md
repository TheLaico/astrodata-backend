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

Para desarrollo local, deja estas variables en `.env`:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=astrodata_lab
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
NASA_API_KEY=DEMO_KEY
```

Las dependencias de embeddings se instalan aparte:

```powershell
pip install -r requirements-ml.txt
```

`requirements-ml.txt` usa `fastembed`, evitando la instalacion pesada de PyTorch.

## Instalar y preparar Ollama

Descarga Ollama para Windows desde:

```text
https://ollama.com/download/windows
```

Despues de instalarlo, cierra y abre PowerShell. Verifica:

```powershell
ollama --version
ollama pull llama3.2
ollama list
```

Tambien puedes comprobar que el servidor local responde en:

```text
http://localhost:11434/api/tags
```

Si `POST /api/chat/preguntar` devuelve `503`, normalmente significa que Ollama no esta corriendo o que el modelo `llama3.2` no esta descargado.

## Ejecutar servidor

```powershell
uvicorn app.main:app --reload
```

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
python -m app.seed.seed_objetos_celestes
```

El seed inicial carga objetos astronomicos base en la coleccion `celestial_objects`.

## Crear indices

Despues de configurar `MONGODB_URI` en `.env`, ejecuta:

```powershell
python -m app.seed.crear_indices
```

El script crea indices normales para `celestial_objects`, `documents`, `document_chunks` y `query_history`. Tambien imprime la definicion del indice de MongoDB Atlas Vector Search para `document_chunks.embedding`.

El archivo de referencia del indice vectorial esta en:

```text
app/seed/atlas_vector_search_index.json
```

## Seed APOD

Despues de configurar `MONGODB_URI` y `NASA_API_KEY` en `.env`, ejecuta:

```powershell
python -m app.seed.seed_apod_documentos
```

Este seed consulta NASA APOD, guarda documentos crudos en `documents` y divide las explicaciones en chunks dentro de `document_chunks`. En esta fase los chunks quedan con `embedding=None`; los embeddings se generan en el siguiente modulo.

## Generar embeddings

Despues de cargar APOD, ejecuta:

```powershell
pip install -r requirements-ml.txt
python -m app.seed.generar_embeddings_chunks
```

Este proceso usa `sentence-transformers/all-MiniLM-L6-v2` mediante `fastembed` para completar el campo `embedding` de cada documento en `document_chunks`. El modelo genera vectores de 384 dimensiones.

En MongoDB local, el chat usa un fallback de similitud coseno en Python. En MongoDB Atlas, puede usar Atlas Vector Search con el indice definido en `app/seed/atlas_vector_search_index.json`.

## Flujo recomendado de preparacion

```powershell
python -m app.seed.crear_indices
python -m app.seed.seed_objetos_celestes
python -m app.seed.seed_apod_documentos
pip install -r requirements-ml.txt
python -m app.seed.generar_embeddings_chunks
uvicorn app.main:app --reload
```

Antes de usar `POST /api/chat/preguntar`, verifica:

- `GET /api/db/ping` responde con `conectado: true`.
- `GET /api/stats` muestra documentos, chunks y chunks con embedding.
- Ollama responde en `http://localhost:11434/api/tags`.
- `OLLAMA_MODEL` coincide con un modelo listado por `ollama list`.

Con MongoDB local no necesitas Atlas Vector Search para la demo: el backend usa fallback local con similitud coseno. Si despliegas en MongoDB Atlas, configura el indice vectorial usando `app/seed/atlas_vector_search_index.json`.

## Terminal de BD

`POST /api/db/query` permite consultas controladas sobre MongoDB para la seccion administrativa. Soporta:

- `find`
- `aggregate`
- `count_documents`

Solo permite las colecciones del proyecto y bloquea operadores peligrosos como `$where`, `$function`, `$out` y `$merge`.

## Ejecutar pruebas

```powershell
pip install -r requirements-dev.txt
pytest
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
