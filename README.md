Kélvin Elí Ramírez Ponciano
000131643
Examen Final

INICIAR
cd quicktickets
docker compose down -v (Para detener servicios anteriores)
docker compose up -d --scale api=3 build
docker compose ps


PRUEBAS EN POSTMAN:
Get a http://localhost:8080/health

Crear ticket:
post a http://localhost:8080/tickets
Header:
Content-Type: application/json
Body:

{
  "client_id": "C123",
  "subject": "Error en login",
  "description": "No puedo iniciar sesión",
  "priority": "alta"
}

Obtener tickets:
Get a http://localhost:8080/tickets

Obtener ticket por ID:
Get a http://localhost:8080/tickets/1

Apagar servicios:
docker compose down -v
