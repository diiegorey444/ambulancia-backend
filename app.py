import psycopg2, os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Render inyecta la URL de conexión de la base de datos como variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def home():
    return "API del sistema de ambulancias funcionando en Render."

@app.route('/api/accidentes', methods=['POST'])
def registrar_accidente():
    data = request.get_json()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accidentes (nombre, telefono, descripcion, latitud, longitud) VALUES (%s, %s, %s, %s, %s)",
        (data['nombre'], data['telefono'], data['descripcion'], data['latitud'], data['longitud'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Accidente registrado correctamente'}), 201

@app.route('/api/accidentes', methods=['GET'])
def obtener_accidentes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accidentes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    accidentes = []
    for row in rows:
        accidentes.append({
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'descripcion': row[3],
            'latitud': row[4],
            'longitud': row[5]
        })
    return jsonify(accidentes)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10000)

