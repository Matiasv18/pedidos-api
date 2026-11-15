from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
PEDIDO = {
    "cliente": "Ana Pérez",
    "direccion_envio": "Calle 10 #5-20, Bogotá",
    "productos": [{"producto": "Teclado", "cantidad": 2}],
}


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_crear_y_listar():
    r = client.post("/pedidos", json=PEDIDO)
    assert r.status_code == 201
    assert r.json()["estado"] == "Pendiente"
    assert len(client.get("/pedidos").json()) >= 1


def test_actualizar_estado_y_filtrar():
    pid = client.post("/pedidos", json=PEDIDO).json()["id"]
    r = client.patch(f"/pedidos/{pid}/estado", json={"estado": "Enviado"})
    assert r.json()["estado"] == "Enviado"
    enviados = client.get("/pedidos", params={"estado": "Enviado"}).json()
    assert any(p["id"] == pid for p in enviados)


def test_validaciones():
    assert client.post("/pedidos", json={**PEDIDO, "productos": []}).status_code == 422
    assert client.get("/pedidos/no-existe").status_code == 404
