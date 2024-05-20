from backend.db import mysql
from flask import Flask

# Crie uma instância do aplicativo Flask
app = Flask(__name__)

# Função para extrair parâmetros de uma mensagem
def extrair_parametros(partes):
    parametros = []
    for parte in partes:
        if "(" in parte and ")" in parte:
            parametros_str = parte[parte.find("(") + 1: parte.find(")")]
            parametros.extend(parametros_str.split(","))
    return parametros

def processar_sql(mensagem):
    try:
        codigo_sql = mensagem.split("CODIGO SQL121:")
        codigo_sql = " ".join(codigo_sql)
        codigo_sql = codigo_sql.replace("```", "").strip()
        codigo_sql = codigo_sql.replace("CODIGO SQL121:", "").strip()
        codigo_sql = codigo_sql[codigo_sql.find("SELECT"):]
        cursor = mysql.connection.cursor()
        cursor.execute(parte)
        resultado = cursor.fetchall()
        cursor.close()
        resultado_final = '\n'.join([str(a) for a in resultado])
        return resultado_final
    except Exception as e:
        return "Erro ao executar o código SQL: " + str(e)