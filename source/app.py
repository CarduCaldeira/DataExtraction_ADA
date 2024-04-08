from flask import Flask, jsonify, request, render_template
import schedule
from utils import update_db_silver, update_raw_db, check_valide_date, get_number_news_bd, load_db
import calendar
from flask_wtf.csrf import CSRFProtect
import threading
import time


app = Flask(__name__, template_folder='templates')  # instância o método Flask
csrf = CSRFProtect(app)


# Routes
@app.route('/')
def homepage():
    return render_template("index.html")


# OK
@app.route('/allnews')
def all_news():
    query = "SELECT id, title, description FROM silver_db.news;"
    df_news = load_db(query)
    dict_news = df_news.to_dict(orient='records')
    return render_template("all_news.html", tabela=dict_news)


# OK
@app.route('/news_by_day')
def news_by_day():
    query = ("SELECT EXTRACT(month FROM publication_date) AS month, EXTRACT(day FROM publication_date) AS day, COUNT(*)"
             "FROM silver_db.news "
             "GROUP BY month, day "
             "ORDER by month, day;")
    df_news = load_db(query)
    df_news['day'] = df_news['day'].astype(int)
    df_news['month'] = df_news['month'].astype(int)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_day.html", tabela=dict_news)

# OK
@app.route('/news_by_month')
def news_by_month():
    query = ("SELECT EXTRACT(month FROM publication_date) AS month, COUNT(*) "
             "FROM silver_db.news "
             "GROUP BY month "
             "ORDER by month")
    df_news = load_db(query)
    df_news['month'] = df_news['month'].astype(int)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_month.html", tabela=dict_news)


# OK
@app.route('/news_by_year')
def news_by_year():
    query = ("SELECT EXTRACT(year FROM publication_date) AS year, COUNT(*) "
             "FROM silver_db.news "
             "GROUP BY year "
             "ORDER by year")
    df_news = load_db(query)
    df_news['year'] = df_news['year'].astype(int)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_year.html", tabela=dict_news)


@app.route('/news_by_author')
def news_by_author():
    query = ("""SELECT silver_db.authors.name, COUNT(silver_db.news.id) AS article_count
        FROM silver_db.news
        JOIN silver_db.authors ON silver_db.authors.id = news.author_id
        GROUP BY silver_db.authors.name
        ORDER BY article_count DESC""")
    df_news = load_db(query)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_author.html", tabela=dict_news)


@app.route('/news_by_source')
def news_by_source():
    query = ("""SELECT silver_db.sources.name, COUNT(silver_db.news.id) AS source_count
        FROM silver_db.news
        JOIN silver_db.sources ON silver_db.sources.id = news.source_id
        GROUP BY silver_db.sources.name
        ORDER BY source_count DESC;""")
    df_news = load_db(query)
    dict_news = df_news.to_dict(orient='records')
    return render_template("news_by_source.html", tabela=dict_news)


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

    schedule.every().hour.at(":52").do(update_raw_db)
    schedule.every().day.at("16:53").do(update_db_silver)
    port = 5000

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    try:
        app.run(port=port)

    except KeyboardInterrupt:
        print('Detected keyboard interrupt, stopping Flask...')
