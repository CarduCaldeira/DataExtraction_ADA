import requests
import pandas as pd

def get_articles(api_url: str, api_key: str) -> pd.DataFrame: 
    """Obtem artigos de notícias usando a API de notícias.

     Parâmetros:
     api_url (str): o URL base da API de notícias.
     api_key (str): A chave API para acessar a API News.

     Retorna:
     pd.DataFrame: Um DataFrame do pandas contendo os artigos de notícias recuperados.
     """
    params = {'q': 'Apple', 'apiKey': api_key}
    response = requests.get(api_url, params=params)
    articles = response.json()['articles']
    dataframe = pd.json_normalize(articles)
    return dataframe


def transforming_articles(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
     Transforma um DataFrame de artigos de notícias removendo linhas onde a
     coluna é '[Removed]' ou None e retorna o DataFrame modificado.

     Parâmetros:
     dataframe (pd.DataFrame): O DataFrame de artigos de notícias a serem transformados.

     Retorna:
     pd.DataFrame: O DataFrame modificado com linhas removidas onde está '[Removed]' ou None.
     """
     
    # Cria uma lista com as colunas do DataFrame que serão verificadas para remover os valores '[Removed]' ou None
    new_columns = [col for col in dataframe.columns if col not in ['urlToImage', 'source.id']]

    # Remove as linhas do DataFrame das colunas que possuem os valores '[Removed]' ou None
    for col in new_columns:
        remove_mask = (dataframe[col] == '[Removed]') | (
            dataframe[col].isnull())
        dataframe = dataframe[~remove_mask]

    return dataframe

