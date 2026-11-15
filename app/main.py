from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="API de Gestión de Pedidos")


class Estado(str, Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    ENVIADO = "Enviado"
    ENTREGADO = "Entregado"


class Item(BaseModel):
    producto: str
    cantidad: int = Field(gt=0)


class PedidoIn(BaseModel):
    cliente: str
    direccion_envio: str
    productos: list[Item] = Field(min_length=1)


class EstadoIn(BaseModel):
    estado: Estado


PEDIDOS: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: PedidoIn):
    pid = str(uuid4())
    PEDIDOS[pid] = {
        "id": pid,
        **pedido.model_dump(mode="json"),
        "estado": Estado.PENDIENTE.value,
        "fecha_creacion": datetime.now(timezone.utc).isoformat(),
    }
    return PEDIDOS[pid]


@app.get("/pedidos")
def listar_pedidos(
    estado: Optional[Estado] = None,
    ordenar_por: str = Query("fecha_creacion", pattern="^(fecha_creacion|cliente|estado)$"),
    orden: str = Query("desc", pattern="^(asc|desc)$"),
):
    datos = list(PEDIDOS.values())
    if estado:
        datos = [p for p in datos if p["estado"] == estado.value]
    return sorted(datos, key=lambda p: p[ordenar_por], reverse=(orden == "desc"))


@app.get("/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: str):
    if pedido_id not in PEDIDOS:
        raise HTTPException(404, "Pedido no encontrado")
    return PEDIDOS[pedido_id]


@app.patch("/pedidos/{pedido_id}/estado")
def actualizar_estado(pedido_id: str, body: EstadoIn):
    if pedido_id not in PEDIDOS:
        raise HTTPException(404, "Pedido no encontrado")
    PEDIDOS[pedido_id]["estado"] = body.estado.value
    return PEDIDOS[pedido_id]
