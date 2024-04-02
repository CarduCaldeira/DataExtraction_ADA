import os
from dotenv import load_dotenv
from typing import Dict


def config_db() -> Dict:
       
    load_dotenv("./.env_db")

    dict_param ={'dbname': os.getenv("DB_NAME"),
                'user': os.getenv("DB_USER"),
                'password': os.getenv("DB_PASSWORD"),
                'host': os.getenv("DB_HOST")}
    
    return dict_param

def config_url() -> Dict:
    
    load_dotenv("./.env")

    dict_param ={'key_password': os.getenv("KEY_PASSWORD"),
                'query_1': os.getenv("QUERY1"),
                'query_2': os.getenv("QUERY2"),
                'query_3': os.getenv("QUERY3")}
    
    return dict_param