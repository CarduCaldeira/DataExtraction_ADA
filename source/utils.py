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
    
    #pega a informação do raw_db e salva do db
    pass


def update_raw_db() -> None:
    """
    Cada uma hora faz request 
    """
    url = create_url_filter(True)
    
    response = requests.get(url)

    if response.status_code == 200:
        
        response = response.json()
        insert_request_df(pd.json_normalize(response["articles"]))
        
def create_url_filter(filter: bool, date: Union[str, None] = None) -> str:
    """
    Cria url pra request
    """
    if filter:
        date = "2024-03-20"
        params = config_url()
        q1 = params["query_1"]
        q2 = params["query_2"]
        q3 = params["query_3"]
        password = params["key_password"]

        url = f"https://newsapi.org/v2/everything?q=({q1} AND {q2})&from={date}&sortBy=publishedAt&apiKey={password}&page=5"
    
    else:
        url = f"https://newsapi.org/v2/everything?from={date}&sortBy=publishedAt&apiKey={password}"

    return url

def insert_request_df(df:pd.DataFrame) -> None:

    """
    configura e faz inserçao a partir de um df
    """
    
    params = config_db()
    print('Connecting to the postgreSQL database ...')
    connection = psycopg2.connect(**params)

    # create a cursor
    cursor = connection.cursor()

    try:
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerows(df.values)
        sio.seek(0)

        
        cursor.copy_expert(
                sql="""
                COPY noticias (
                    autor, 
                    titulo, 
                    descricao, 
                    url, 
                    imagem_url, 
                    data_publicacao,
                    conteudo,
                    tags,
                    fonte
                ) FROM STDIN WITH CSV""",
                file=sio
            )

        # Commit da transação
        connection.commit()

        print("Registro inserido com sucesso!")

    except psycopg2.Error as e:
        print("Erro ao inserir o registro:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def check_valide_date(data: str) -> bool:
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True 
    except ValueError:
        return False  

def get_number_news(date_from :str, date_to : Union[str, None] = None):
    pass

def get_number_news_bd(date_from :str, date_to : Union[str, None] = None):
    pass
