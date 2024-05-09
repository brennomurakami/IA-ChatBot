from backend.db import mysql
from flask import Flask

# Crie uma instância do aplicativo Flask
app = Flask(__name__)

# Função para retornar dados de vendas por período
def dados_vendas_por_periodo(inicio, fim):
    consulta = (
        "SELECT SUM(valor_total) AS total_vendas, AVG(valor_total) AS media_vendas "
        "FROM vendas "
        "WHERE data_venda BETWEEN %s AND %s"
    )
    cursor = mysql.connection.cursor()
    cursor.execute(consulta, (inicio, fim))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

# Função para retornar os melhores clientes
def melhores_clientes():
    consulta = (
        "SELECT c.nome_cliente, SUM(v.valor_total) AS total_compras "
        "FROM clientes c "
        "JOIN vendas v ON c.id = v.id_cliente "
        "GROUP BY c.nome_cliente "
        "ORDER BY total_compras DESC"
    )
    cursor = mysql.connection.cursor()
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    resultado = "\n".join(str(a) for a in resultados)
    return resultado

# Função para retornar o protocolo de inseminação mais utilizado
def protocolo_mais_utilizado():
    consulta = (
        "SELECT id_protocolo, COUNT(*) AS quantidade "
        "FROM resultados_inseminacao "
        "GROUP BY id_protocolo "
        "ORDER BY quantidade DESC "
        "LIMIT 1"
    )
    cursor = mysql.connection.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

def fazendas_nao_visidadas_mes_atual():
    consulta = (
    "SELECT f.id, f.nome_fazenda "
    "FROM Fazendas f "
    "WHERE EXISTS ( "
    "SELECT 1 " 
    "FROM Visitas v "
    "WHERE f.id = v.id_fazenda " 
    "AND EXTRACT(MONTH FROM v.data_visita) != EXTRACT(MONTH FROM CURRENT_DATE))"
    )
    cursor = mysql.connection.cursor()
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    resultado = "\n".join(str(a) for a in resultados)
    return resultado

# Função para calcular o percentual de vacas que não engravidaram após a inseminação
def percentual_vazias():
    consulta_total = "SELECT COUNT(*) FROM vacas"
    cursor = mysql.connection.cursor()
    cursor.execute(consulta_total)
    cursor.close()
    total_vacas = cursor.fetchone()[0]

    consulta_vazias = "SELECT COUNT(*) FROM resultados_inseminacao WHERE vazia_Com_Ou_Sem_CL = 1"
    cursor = mysql.connection.cursor()
    cursor.execute(consulta_vazias)
    vacas_vazias = cursor.fetchone()[0]
    cursor.close()
    percentual = (vacas_vazias / total_vacas) * 100
    return percentual

def obter_resultados_inseminacao_ordenados_por_data():
    consulta = (
    "SELECT " 
    "ri.id AS id_resultado, "
    "ri.data_inseminacao, "
    "fi.nome_fazenda AS fazenda, "
    "ins.nome_inseminador AS inseminador, "
    "v.numero_animal AS numero_vaca, "
    "v.vaca, "
    "t.nome_touro AS touro, "
    "pi.protocolo AS protocolo, "
    "ri.numero_IATF, "
    "CASE ri.DG WHEN 1 THEN 'Sim' ELSE 'Não' END AS prenha, "
    "CASE ri.vazia_Com_Ou_Sem_CL WHEN 1 THEN 'Com CL' ELSE 'Sem CL' END AS status_gestacional, "
    "CASE ri.perda WHEN 1 THEN 'Sim' ELSE 'Não' END AS perda_gestacional "
    "FROM resultados_inseminacao AS ri "
    "JOIN vacas AS v ON ri.id_vaca = v.id "
    "JOIN fazendas AS fi ON v.id_fazenda = fi.id "
    "JOIN protocolos_inseminacao AS pi ON ri.id_protocolo = pi.id "
    "JOIN touros AS t ON ri.id_touro = t.id "
    "JOIN inseminadores AS ins ON ri.id_inseminador = ins.id "
    "ORDER BY ri.data_inseminacao DESC;"
    )
    cursor = mysql.connection.cursor()
    cursor.execute(consulta)
    cursor.close()
    total_vacas = cursor.fetchall()
    resultado = "\n".join(str(a) for a in total_vacas)
    return resultado

# Função para processar as mensagens do usuário
def processar_funcoes(mensagem):
    funcoes_disponiveis = {
        "dados_vendas_por_periodo": dados_vendas_por_periodo,
        "melhores_clientes": melhores_clientes,
        "protocolo_mais_utilizado": protocolo_mais_utilizado,
        "fazendas_nao_visidadas_mes_atual": fazendas_nao_visidadas_mes_atual,
        "percentual_vazias": percentual_vazias
    }

    # Remove a parte "FUNCOES NECESSARIAS:" da mensagem
    mensagem = mensagem.replace("FUNCOES NECESSARIAS:", "").strip()

    # Divide a mensagem com base em "||" para processar funções ou SQL separadamente
    partes = mensagem.split("||")

    resultados = []
    for parte in partes:
        parte = parte.strip()
        # Verifica se é uma função
        for funcao_nome, funcao in funcoes_disponiveis.items():
            if funcao_nome in parte:
                parametros = None
                if "dados_vendas_por_periodo" in parte:
                    parametros_str = parte[parte.find("(") + 1: parte.find(")")]
                    parametros = parametros_str.split(",")
                resultado = funcao() if not parametros else funcao(*parametros)
                resultados.append((funcao_nome, resultado))

    resposta = " ".join([f"Função {funcao}: Resultado {resultado}" for funcao, resultado in resultados])
    return resposta


# Função para extrair parâmetros de uma mensagem
def extrair_parametros(partes):
    parametros = []
    for parte in partes:
        if "(" in parte and ")" in parte:
            parametros_str = parte[parte.find("(") + 1: parte.find(")")]
            parametros.extend(parametros_str.split(","))
    return parametros

def processar_sql(mensagem):
    codigo_sql = mensagem.split("CODIGO SQL121:")
    codigo_sql = " ".join(codigo_sql)
    codigo_sql = codigo_sql.replace("CODIGO SQL121:", "").strip()
    codigo_sql = codigo_sql[codigo_sql.find("SELECT"):]
    partes = codigo_sql.split("||")
    for parte in partes:     
        cursor = mysql.connection.cursor()
        cursor.execute(parte)
        resultado = cursor.fetchall()
        cursor.close()
        resultado_final = '\n'.join([str(a) for a in resultado])
    return resultado_final
    
def processar_mensagem(mensagem):
    # Dividir a mensagem em partes separadas por '||'
    partes = mensagem.split("||")
    
    # Inicializar as variáveis para armazenar as partes separadas
    funcoes_parte = None
    sql_parte = None
    
    # Verificar se há partes específicas para funções e SQL
    for parte in partes:
        if "FUNCOES NECESSARIAS" in parte:
            funcoes_parte = parte
        elif "CODIGO SQL" in parte:
            sql_parte = parte
    
    # Processar a parte das funções, se presente
    if funcoes_parte:
        resultado_funcoes = processar_funcoes(funcoes_parte)
    else:
        resultado_funcoes = ""
    
    # Processar a parte do SQL, se presente
    if sql_parte:
        resultado_sql = processar_sql(sql_parte)
    else:
        resultado_sql = ""
    
    # Combinar os resultados das funções e do SQL
    resposta = resultado_funcoes + " " + resultado_sql
    return resposta