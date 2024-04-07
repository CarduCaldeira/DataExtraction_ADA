import requests
import pandas as pd
import psycopg2
from config import config_db, config_url
import csv
from io import StringIO
import datetime
from typing import Union


def update_db() -> None:
    """
    Uma vez por dia sumariza as informaçoes 
    do raw_db em um db processado
    """

    # pega a informação do raw_db e salva do db
    pass


def update_raw_db() -> None:
    """
    Cada uma hora faz request para a API e insere os dados em um DataFrame.

    Esta função faz uma requisição HTTP para a API fornecida pelo método `create_url_filter()`
    e insere os dados na base de dados definida no arquivo `config.py`.
    """

    # Cria a URL para a requisição da API
    url = create_url_filter()

    # Faz a requisição HTTP para a API
    response = requests.get(url)

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:

        # Converte a resposta em JSON e insere os dados na base de dados
        response = response.json()
        insert_request_df(pd.json_normalize(response["articles"]))


def create_url_filter(date: Union[str, None] = None) -> str:
    """
    Cria a URL para a requisição.

    Esta função recebe um parâmetro opcional 'data' que representa a data
    dos artigos de notícias. Se nenhuma data for fornecida, ela assume a data
    atual do sistema no formato 'AAAA-MM-DD'.

    Args:
        data (str ou None): A data dos artigos de notícias. O valor padrão é None.

    Retorna:
        str: A URL completa para a requisição.
    """

    # Define a data padrão se nenhuma data for fornecida ou estiver no formato incorreto.
    # if check_valide_date(date) == False or date is None:
    #     date = datetime.today().strftime("%Y-%m-%d")

    date = '2024-04-02'

    # Obtém os parâmetros de configuração
    params = config_url()
    q1 = params["query_1"]
    q2 = params["query_2"]
    q3 = params["query_3"]
    senha = params["key_password"]

    # Construção da URL
    url = (
        f'https://newsapi.org/v2/everything?q=Apple&'
        f'from=2024-04-02&language=en&sortBy=publishedAt&apiKey=948867445882452ea34165f1f41fabaf&page=5'

    )

    return url


def insert_request_df(df: pd.DataFrame) -> None:
    """
    Insere um dataframe em um banco de dados PostgreSQL.

    Args:
        df (pd.DataFrame): O dataframe a ser inserido.

    Esta função se conecta a um banco de dados PostgreSQL, cria um cursor, 
    converte o dataframe para uma string CSV, escreve a string CSV em um 
    objeto StringIO e usa o cursor para inserir os dados CSV na tabela 
    'noticias'.

    Lança:
        psycopg2.Error: Se houver erro ao inserir o registro.

    Retorna:
        None
    """

    # Obtém a configuração do banco de dados
    params = config_db()

    # Conecta-se ao banco de dados
    print('Conectando ao banco de dados PostgreSQL ...')
    connection = psycopg2.connect(**params)

    # Cria um cursor
    cursor = connection.cursor()

    try:
        # Converte dataframe para string CSV
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerows(df.values)
        sio.seek(0)

        # Insere dados CSV no banco de dados
        cursor.copy_expert(
            sql="""COPY raw_db.news (
                    author, 
                    title, 
                    description, 
                    url, 
                    image_url, 
                    publication_date,
                    content,
                    tags,
                    source
                ) FROM STDIN WITH CSV""",
            file=sio
        )

        # Confirma a transação
        connection.commit()

        print("Registro inserido com sucesso!")

    except psycopg2.Error as e:
        print("Erro ao inserir o registro:", e)

    finally:
        # Fecha o cursor e a conexão
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def check_valide_date(date: str) -> bool:
    """
    Verifica se uma determinada data está no formato 'AAAA-MM-DD'.

    Args:
        date (str): A data a ser verificada.

    Returns:
        bool: True se a date estiver no formato correto, False caso contrário.
    """

    # Tentamos analisar a data usando o formato '%Y-%m-%d'. Se falhar,
    # retornamos False. Caso contrário, retornamos True.
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def get_number_news_bd(date_from :str, date_to : Union[str, None] = None):
    pass
