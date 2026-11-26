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


if __name__ == "__main__":
    app.run(debug=True, port=8000)