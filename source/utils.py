import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text, quoted_name
from config import config_db, config_url
import csv
from io import StringIO
from datetime import datetime, timedelta
from typing import Union, List


def update_db_silver() -> None:
    """
    Uma vez por dia sumariza as informaçoes 
    do raw_db em um db processado
    """

    params = config_db()

    try:
        with open('consulta.sql', 'r') as file:
            sql_query = file.read()

        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}")
        df = pd.read_sql(sql_query, engine)

        df = df[['title','author','description','url','publication_date', 'source','query0','query1','query2']]
        df.dropna(subset=['title', 'url', 'author', 'publication_date', 'source'], inplace =True)

        insert_source(df)
        insert_author(df)

        df = execute_join_source(df)
        df = execute_join_author(df)

        with engine.connect() as conn:
            for _, row in df.iterrows():
            
                escaped_title = escape_string(row['title'])
                escaped_description = escape_string(row['description'])
                escaped_url = escape_string(row['url'])
                #escaped_publication_date = escape_string(row['publication_date'])

                query = text(f"""
                    INSERT INTO silver_db.news (title, description, url, publication_date, query0, query1, query2, source_id, author_id)
                    VALUES ('{escaped_title}', '{escaped_description}', '{escaped_url}', '{row['publication_date']}', '{row['query0']}', '{row['query1']}', '{row['query2']}', '{row['source_id']}', '{row['author_id']}')
                    ON CONFLICT (title, url) DO NOTHING;
                    """)
                conn.execute(query)  # Passando os valores do DataFrame para a consulta SQL

            # Confirmar a transação após inserções
            conn.commit()

        print("Dados inseridos com sucesso!")

    except Exception as e:
        print("Erro ao inserir dados:", e)


def update_raw_db() -> None:
    """
    Cada uma hora faz request para a API e insere os dados em um DataFrame.

    Esta função faz uma requisição HTTP para a API fornecida pelo método `create_url_filter()`
    e insere os dados na base de dados definida no arquivo `config.py`.
    """
    
    # Cria uma lista de URL para a requisição da API
    urls = create_url_filter()
    df = create_dataframe(urls)

    if df is not None:
        insert_request_df(df)


def create_url_filter(date: Union[str, None] = None) -> List[str]:
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
    urls = []

    # Obtém os parâmetros de configuração
    params = config_url()
    q1 = params["query_1"]
    q2 = params["query_2"]
    q3 = params["query_3"]
    queries = [q1, q2, q3]
    password = params["key_password"]
    from_date, to_date = calculate_date()
    
    # Construção da URL
    for query in queries:    
        
        url = (
            f'https://newsapi.org/v2/everything?q={query}'
            f'&language=en&apiKey={password}' #from={from_date}&to={to_date}&language=en&sortBy=publishedAt
        )
        urls.append(url)

    return urls

def create_dataframe(urls: List[str]) -> Union[pd.DataFrame, None]:

    df_list = []

    for i, url in enumerate(urls):
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            articles_df = pd.json_normalize(response["articles"])
            
            # Criar as colunas e preencher com 0
            articles_df["query0"] = 0
            articles_df["query1"] = 0
            articles_df["query2"] = 0
            
            # Preencher com 1 com base no valor de i
            if i == 0:
                articles_df["query0"] = 1
            elif i == 1:
                articles_df["query1"] = 1
            elif i == 2:
                articles_df["query2"] = 1
            
            df_list.append(articles_df)

    # Concatenar todos os DataFrames da lista em um único DataFrame final
    df = pd.concat(df_list, ignore_index=True)

    if df is not None:
        return df
    
    return None


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
                    source,
                    query0,
                    query1,
                    query2
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

def insert_source(df: pd.DataFrame) -> None:
    
    source_values = pd.unique(df['source'])
    params = config_db()

    try:
        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}")
        with engine.connect() as conn:
        # Inserindo os dados na tabela authors com a cláusula ON CONFLICT
            for linha in source_values:
                query = text(f"""
                    INSERT INTO silver_db.sources ("name")
                    VALUES ('{linha}')
                    ON CONFLICT (name) DO NOTHING;
                """)
                conn.execute(query)
            conn.commit()
 
        print("Dados inseridos na tabela sources com cláusula ON CONFLICT!")

    except Exception as e:
        print("Erro ao inserir dados na tabela sources:", e)


def insert_author(df: pd.DataFrame) -> None:
    
    author_values = pd.unique(df['author'])
    params = config_db()

    try:
        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}")
        with engine.connect() as conn:
        # Inserindo os dados na tabela authors com a cláusula ON CONFLICT
            for linha in author_values:
                linha_escaped = linha.replace("'", "''")

                query = text(f"""
                    INSERT INTO silver_db.authors (name)
                    VALUES ('{linha_escaped}')
                    ON CONFLICT (name) DO NOTHING
                """)
                conn.execute(query)
            conn.commit()

        print("Dados inseridos na tabela authors com cláusula ON CONFLICT!")

    except Exception as e:
        print("Erro ao inserir dados na tabela authors:", e)

def execute_join_source(df: pd.DataFrame):
    
    params = config_db()

    try:
        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}")
        # Inserindo os dados na tabela authors com a cláusula ON CONFLICT
        query = text("""
            SELECT id as source_id, name
            FROM silver_db.sources
        """)
        df_source = pd.read_sql_query(query, engine)
        df_final = pd.merge(df, df_source, left_on='source', right_on='name', how='inner')
        df_final.drop(columns=['source','name'], inplace=True)

    except Exception as e:
        print("Erro ao fazer a query:", e)
    
    return df_final

def execute_join_author(df: pd.DataFrame):
    
    params = config_db()

    try:
        engine = create_engine(f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}")
        # Inserindo os dados na tabela authors com a cláusula ON CONFLICT
        query = text("""
            SELECT id as author_id, name
            FROM silver_db.authors
        """)
        df_source = pd.read_sql_query(query, engine)
        df_final = pd.merge(df, df_source, left_on='author', right_on='name', how='inner')
        df_final.drop(columns=['author','name'], inplace=True)

    except Exception as e:
        print("Erro ao fazer a query:", e)
    
    return df_final

def calculate_date():
    
    time_now = datetime.now()

    # Calculando 1 dia e 1 hora atrás
    one_day_and_one_hour_ago = time_now - timedelta(days=1, hours=1)
    one_day_ago = time_now - timedelta(days=1)

    # Formatação para o formato desejado
    formato_desejado = "%Y-%m-%dT%H:%M:%S"

    one_day_and_one_hour_ago = one_day_and_one_hour_ago.strftime(formato_desejado)
    one_day_ago = one_day_ago.strftime(formato_desejado)

    return one_day_and_one_hour_ago, one_day_ago

def get_number_news_bd():
    pass

def escape_string(value):
    """Escapa uma string substituindo aspas simples por duas aspas simples."""
    return value.replace("'", "''")


def load_db(sql_query):  # Modificar essa função para que ela receba a query e puxe os dados no db normalizado
    params = config_db()
    conn_string = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"
    engine = create_engine(conn_string)
    dataframe = pd.read_sql_query(sql_query, engine)
    engine.dispose()
    return dataframe
