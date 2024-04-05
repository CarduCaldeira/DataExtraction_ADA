from flask import Flask, jsonify, request, render_template
import schedule
from utils import update_db, update_raw_db, check_valide_date, get_number_news_bd, load_db
import calendar
from flask_wtf.csrf import CSRFProtect
import threading
import time


app = Flask(__name__, template_folder='templates')  # instância o método Flask
csrf = CSRFProtect(app)



# Rotas para acesso visual aos dados extraidos da APINews e inseridos no banco de dados...
@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/allnews')
def all_news():
    query = "SELECT id, autor FROM noticias;"
    df_news = load_db(query)
    dict_news = df_news.to_dict(orient='records')
    return render_template("all_news.html", tabela=dict_news)


@app.route('/news_by_dia')
def news_by_day():
    query = ("SELECT EXTRACT(month FROM data_publicacao) AS mes, EXTRACT(day FROM data_publicacao) AS dia, COUNT(*) "
              "FROM noticias "
             "GROUP BY mes, dia "
             "ORDER by mes, dia;")
    df_news = load_db(query)
    df_news['dia'] = df_news['dia'].astype(int)
    df_news['mes'] = df_news['mes'].astype(int)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_day.html", tabela=dict_news)


@app.route('/news_by_mes')
def news_by_month():
    query = ("SELECT EXTRACT(month FROM data_publicacao) AS mes, COUNT(*) "
             "FROM noticias "
             "GROUP BY mes "
             "ORDER by mes")
    df_news = load_db(query)
    df_news['mes'] = df_news['mes'].astype(int)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_month.html", tabela=dict_news)


# item 4.1
@app.route("/<int:day>/<int:month>", methods=["GET"])
def get_count_of_news_for_day(day: int, month: int, year: int):
    """
    Retorna o numero de noticias naquele dia
    """

    if check_valide_date(f"{2024}-{month}-{day}"):

        n = get_number_news_bd(f"{2024}-{month}-{day}")
        message = {"Quantidade de Noticias": n}
        return jsonify(message)

    message = {"message": "Data Invalida"}
    return jsonify(message)

# item 4.1


@app.route("/<int:month>", methods=["GET"])
def get_count_of_news_for_month(month: int, year: int = 2024):
    """
    Retorna o numero de noticias naquele mes
    """

    n_days = calendar.monthrange(year, month)[1]
    n = get_number_news_bd(f"{year}-{month}-{1}", f"{year}-{month}-{n_days}")
    message = {"Quantidade de Noticias": n}
    return jsonify(message)

# item 4.2


@app.route("/<autor>/<fonte>", methods=["GET"])
def get_count_of_news_for_author_source(autor: str, fonte: str):
    pass

# item 4.3


@app.route("/filtro/<int:day>/<int:month>", methods=["GET"])
def get_count_of_filter_news_for_day(day: int, month: int, year: int = 2024):
    """
    Retorna o numero de noticias pra cada uma das tres queries naquele dia
    """

    if check_valide_date(f"{2024}-{month}-{day}"):

        n = get_number_news_bd(f"{2024}-{month}-{day}")
        message = {"Quantidade de Noticias Filtradas": n}
        return jsonify(message)

    message = {"message": "Data Invalida"}
    return jsonify(message)

# item 4.3


@app.route("/filtro/<int:month>", methods=["GET"])
def get_count_of_filter_news_for_month(month: int, year: int = 2024):
    """
    Retorna o numero de noticias pra cada uma das tres queries naquele mes
    """

    n_days = calendar.monthrange(year, month)[1]
    n = get_number_news_bd(f"{year}-{month}-{1}", f"{year}-{month}-{n_days}")
    message = {"Quantidade de Noticias Filtradas": n}
    return jsonify(message)


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == "__main__":

    schedule.every().hour.at(":23").do(update_raw_db)
    schedule.every().day.at("05:00").do(update_db)
    port = 5000

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    try:
        app.run(port=port)

    except KeyboardInterrupt:
        print('Detected keyboard interrupt, stopping Flask...')
