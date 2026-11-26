import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Conexión a MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "CURSOS_CTPI_2026-ESNEIDER")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "APRENDICES_ASTUDILLO")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
aprendices = db[COLLECTION_NAME]


# 10.1. Consultar la cantidad total de aprendices
@app.route("/api/cantidadAprendices", methods=["GET"])
def cantidad_aprendices():
    cantidad = aprendices.count_documents({})
    return jsonify({"CantidadAprendices": cantidad})

# 10.2. Consultar la cantidad de aprendices por nivel de formación
@app.route("/api/cantidadAprendices/<nivel>", methods=["GET"])
def cantidad_aprendices_nivel(nivel):
    nivel_formateado = nivel.upper()
    cantidad = aprendices.count_documents({"NIVEL_DE_FORMACION": nivel_formateado})
    return jsonify({
        "CantidadAprendices": cantidad,
        "Nivel de formación": nivel_formateado
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)