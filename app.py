from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = os.getenv("DB_USER", "qt_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "qt_pass")
DB_NAME = os.getenv("DB_NAME", "quicktickets_db")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.get("/health")
def health():
    instance = os.getenv("HOSTNAME", "unknown")
    return jsonify({"status":"ok", "instance": instance}), 200

def bad_request(msg: str, status:int=400):
    return jsonify({"error": msg}), status

@app.post("/tickets")
def create_ticket():
    if not request.is_json:
        return bad_request("Request must be JSON")
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")
    subject = data.get("subject")
    description = data.get("description")
    priority = data.get("priority")

    if not (client_id or subject):
        return bad_request("Missing 'client_id' or 'subject'")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO ticket (client_id, subject, description, priority)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (client_id, subject, description, priority))
        conn.commit()
        ticket_id = cursor.lastrowid
        cursor.close()
        conn.close()

        balanceador = request.headers.get("Host", "unknown")
        ticket = {
            "id": ticket_id,
            "client_id": client_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "balanceador": balanceador
        }
        return jsonify(ticket), 201
    except Error as e:
        print("[DB] Error:", e)
        return bad_request("Database error", 500)

@app.get("/tickets")
def get_tickets():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_id, subject, description, priority FROM ticket ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        tickets = []
        for r in rows:
            tickets.append({
                "id": r[0],
                "client_id": r[1],
                "subject": r[2],
                "description": r[3],
                "priority": r[4],
                "balanceador": request.headers.get("Host", "unknown")
            })
        return jsonify(tickets), 200
    except Error as e:
        print("[DB] Error:", e)
        return bad_request("Database error", 500)

@app.get("/tickets/<int:ticket_id>")
def get_ticket(ticket_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, client_id, subject, description, priority FROM ticket WHERE id = %s", (ticket_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return bad_request("Ticket not found", 404)
        ticket = {
            "id": row[0],
            "client_id": row[1],
            "subject": row[2],
            "description": row[3],
            "priority": row[4],
            "balanceador": request.headers.get("Host", "unknown")
        }
        return jsonify(ticket), 200
    except Error as e:
        print("[DB] Error:", e)
        return bad_request("Database error", 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)