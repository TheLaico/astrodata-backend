# AstroData Backend

Backend de AstroData Lab construido con FastAPI.

## Configuracion local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` cuando tengas la URI real de MongoDB Atlas.

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
python -m app.seed.generar_embeddings_chunks
```

Este proceso usa `all-MiniLM-L6-v2` para completar el campo `embedding` de cada documento en `document_chunks`. El modelo genera vectores normalizados de 384 dimensiones, compatibles con busqueda por coseno en MongoDB Atlas Vector Search.

## Flujo recomendado de preparacion

```powershell
python -m app.seed.crear_indices
python -m app.seed.seed_objetos_celestes
python -m app.seed.seed_apod_documentos
python -m app.seed.generar_embeddings_chunks
uvicorn app.main:app --reload
```

Antes de usar `POST /api/chat/preguntar`, configura el indice vectorial en MongoDB Atlas usando `app/seed/atlas_vector_search_index.json` y verifica que Ollama este corriendo con el modelo definido en `OLLAMA_MODEL`.

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
