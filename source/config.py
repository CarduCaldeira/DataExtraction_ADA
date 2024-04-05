import os
from dotenv import load_dotenv
from typing import Dict

def config_db() -> Dict:
    """
    Carrega a configuração do banco de dados do arquivo .env_db e a retorna como um dicionário.

    Retorna:
        dict_param (dict): Um dicionário contendo os parâmetros de configuração do banco de dados.
            - dbname (str): O nome do banco de dados.
            - user (str): O nome do usuário do banco de dados.
            - password (str): A senha do banco de dados.
            - host (str): O nome do servidor do banco de dados.
    """

    # Carrega a configuração do banco de dados do arquivo .env_db
    load_dotenv("./.env_db")

    # Cria um dicionário com os parâmetros de configuração do banco de dados
    dict_param = {
        'dbname': os.getenv("DB_NAME"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST")
    }

    return dict_param

def config_url() -> Dict:
    """
    Carrega a configuração da URL do arquivo .env e a retorna como um dicionário.

    Retorna:
        dict_param (dict): Um dicionário contendo os parâmetros de configuração da URL.
            - key_password (str): A senha da chave da API.
            - query_1 (str): A primeira consulta para o endpoint da API.
            - query_2 (str): A segunda consulta para o endpoint da API.
            - query_3 (str): A terceira consulta para o endpoint da API.
    """

    # Carrega a configuração da URL do arquivo .env
    load_dotenv("./.env")

    # Cria um dicionário com os parâmetros de configuração da URL
    dict_param = {
        'key_password': os.getenv("KEY_PASSWORD"),  # A senha da chave da API
        'query_1': os.getgetenv("QUERY1"),  # A primeira consulta para o endpoint da API
        'query_2': os.getenv("QUERY2"),  # A segunda consulta para o endpoint da API
        'query_3': os.getenv("QUERY3")  # A terceira consulta para o endpoint da API
    }

    return dict_param
