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

# 10.6. Listado de aprendices por programa con estado de ficha "Terminada por unificación"
@app.route("/api/terminadaUnificacion/<programa>", methods=["GET"])
def terminada_unificacion(programa):
    programa_formateado = programa.upper()
    filtro = {
        "PROGRAMA": programa_formateado,
        "ESTADO_FICHA": "Terminada por unificación"
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Programa": programa_formateado,
        "Estado_Ficha": "Terminada por unificación",
        "Aprendices": resultado
    })

# 10.7. Listado de aprendices del programa VISUALIZACION DE DATOS USANDO POWER BI (o cualquier programa)
@app.route("/api/aprendicesPrograma/<programa>", methods=["GET"])
def aprendices_por_programa(programa):
    programa_formateado = programa.upper()
    filtro = {
        "PROGRAMA": programa_formateado
    }
    proyeccion = {
        "_id": 0,
        "PROGRAMA": 1,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Programa": programa_formateado,
        "Total_Aprendices": len(resultado),
        "Aprendices": resultado
    })


# 10.8. Cantidad de aprendices de un programa en estado Certificado
@app.route("/api/cantidadCertificadosPrograma/<programa>", methods=["GET"])
def cantidad_certificados_programa(programa):
    programa_formateado = programa.upper()
    filtro = {
        "PROGRAMA": programa_formateado,
        "ESTADO_APRENDIZ": "Certificado"
    }
    cantidad = aprendices.count_documents(filtro)
    return jsonify({
        "Programa": programa_formateado,
        "Estado_Aprendiz": "Certificado",
        "Cantidad": cantidad
    })


# 10.9. Listado de aprendices de una ficha por estado del aprendiz
@app.route("/api/porEstado/<int:ficha>/<estado>", methods=["GET"])
def aprendices_por_estado(ficha, estado):
    patron_estado = estado.strip().replace("o", "[oó]").replace("O", "[oó]")
    filtro = {
        "FICHA": ficha,
        "ESTADO_APRENDIZ": {"$regex": f"^{patron_estado}$", "$options": "i"}
    }
    proyeccion = {
        "_id": 0,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "PROGRAMA": 1,
        "SEGUNDO_APELLIDO": 1
    }
    resultado = list(aprendices.find(filtro, proyeccion))
    return jsonify({
        "Aprendices": resultado,
        "Estado de los Aprendices": estado,
        "Ficha": str(ficha)
    })

# 10.10. Listar los nombres únicos de los programas de COMPLEMENTARIA VIRTUAL
@app.route("/api/programasComplementariaVirtual", methods=["GET"])
def programas_complementaria_virtual():
    lista_programas = aprendices.distinct(
        "PROGRAMA",
        {"NIVEL_DE_FORMACION": "COMPLEMENTARIA VIRTUAL"}
    )
    lista_programas.sort()
    return jsonify({
        "Nivel_Formacion": "COMPLEMENTARIA VIRTUAL",
        "Total_Programas": len(lista_programas),
        "Programas": lista_programas
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)