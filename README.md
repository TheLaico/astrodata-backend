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
