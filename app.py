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

# 10.3. Listar los nombres únicos de programas por nivel de formación
@app.route("/api/programas/<nivel>", methods=["GET"])
def programas_por_nivel(nivel):
    nivel_formateado = nivel.upper()
    lista_programas = aprendices.distinct("PROGRAMA", {"NIVEL_DE_FORMACION": nivel_formateado})
    lista_programas.sort()
    return jsonify({
        "nivel de formación": nivel_formateado,
        "programas": lista_programas
    })
# 10.4. Listar aprendices certificados de un programa (excluyendo _id)
@app.route("/api/certificados/<programa>", methods=["GET"])
def aprendices_certificados(programa):
    programa_formateado = programa.upper()
    filtro = {
        "PROGRAMA": programa_formateado,
        "ESTADO_APRENDIZ": "Certificado"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Aprendices_Certificados": resultado,
        "Programa": programa_formateado
    })


# 10.5. Cantidad limitada de aprendices por ficha en estado "Por certificar" ordenados descendentemente por apellido
@app.route("/api/porCertificar/<int:ficha>/<int:limite>", methods=["GET"])
def aprendices_por_certificar(ficha, limite):
    filtro = {
        "FICHA": ficha,
        "ESTADO_APRENDIZ": "Por certificar"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "PROGRAMA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(
        aprendices.find(filtro, proyeccion)
        .sort("PRIMER_APELLIDO", -1)
        .limit(limite)
    )
    return jsonify({
        "Cantidad de Aprendices por Certificar": resultado
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)