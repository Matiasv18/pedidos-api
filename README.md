# pedidos-api

API REST de gestión de pedidos (FastAPI) con despliegue automático en AWS.

## Endpoints
- `GET /health`: estado del servicio
- `POST /pedidos`: crear pedido
- `GET /pedidos`: listar (filtro `estado`, orden `ordenar_por` y `orden`)
- `GET /pedidos/{id}`: obtener un pedido
- `PATCH /pedidos/{id}/estado`: actualizar estado

## Ejecución local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
uvicorn app.main:app --reload
```
Documentación: http://127.0.0.1:8000/docs
